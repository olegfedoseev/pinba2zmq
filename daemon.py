#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, multiprocessing, itertools, math, errno, traceback

import gevent
from gevent.monkey import patch_all; patch_all()
from gevent.queue import JoinableQueue
from gevent.pool import Pool
from gevent.baseserver import BaseServer
from gevent import socket, core

from gevent_zeromq import zmq as gzmq

from Pinba import Request

class groupby(dict):
    def __init__(self, seq, key=lambda x:x):
        for value in seq:
            self.setdefault(key(value), []).append(value)
    __iter__ = dict.iteritems

def avg(values, cnt=None):
    """ Вычисляет среднее значение """
    return sum(map(float, values)) / (len(values) if cnt is None else cnt)

def stddev(values, cnt=None):
    """ Вычисляет среднеквадратическое отклонение """
    mean = avg(values)
    return (sum((v - mean) ** 2 for v in values) / (len(values) if cnt is None else cnt)) ** 0.5

def median(values):
    """ 
    Вычисляет медиану 
    A median is also known as the 50th percentile. Exactly 50% of people make less than the median and 50% make more.
    """
    return sorted(values)[len(values) / 2]

def percentile(values, percentile=75):
    """
    Вычисляет перцентиль 
    """
    idx = math.trunc(((100 - percentile) / 100) * len(values))
    if idx > 0:
        values = sorted(values)[idx:]
    return sum(values) / len(values)

def aggregate(values, cnt=None):
    """
    Возвращает массив c максимальным значением, 75ти и 85ти процентным перценталем, 
    средним и медианным значениями и среднеквадратичным отклонением.
    Все значения в микросекундах, int
    """
    if cnt is None:
        cnt = len(values)

    if cnt == 0:
        return { 'max': 0, 'p75': 0, 'p85': 0, 'avg': 0, 'med': 0, 'dev': 0 }
    if cnt == 1:
        val = int(values[0] * 1000000)
        return { 'max': val, 'p75': val, 'p85': val, 'avg': val, 'med': val, 'dev': val }

    return {
        'max': int(max(values) * 1000000),
        'p75': int(percentile(values, 75) * 1000000),
        'p85': int(percentile(values, 85) * 1000000),
        'avg': int(avg(values, cnt) * 1000000),
        'med': int(median(values) * 1000000),
        'dev': int(stddev(values, cnt) * 1000000),
    }

class Decoder(multiprocessing.Process):
    def __init__(self, pid):
        multiprocessing.Process.__init__(self)
        self.parent = pid

    def run(self):
        import zmq
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:5042")
        print multiprocessing.current_process().name, 'ready'
        try:
            while True:
                if self.parent is not None and os.getppid() != self.parent:
                    break
                t, raw_requests = socket.recv_pyobj()
                socket.send_pyobj((t, self.group(self.decode(raw_requests))))
        except KeyboardInterrupt:
            pass
        except Exception, e:
            print "Worker get exception: %s, %s" % (type(e), e)

        socket.close()
        context.term()

    def decode(self, rows):
        """
        Decode protobuf packets and format data in usable format

        Return data in format: [((host, server, script), (doc_size, req_time), [timers]), ...]
        """
        requests = []
        for r in rows:
            request = Request()
            request.ParseFromString(r)

            timers = []
            if len(request.timer_hit_count) > 0:
                offset = 0
                for tag_count, hit_count, timer_value in zip(request.timer_tag_count, request.timer_hit_count, request.timer_value):
                    tags = {}
                    to = offset + tag_count
                    for tag_name, tag_value in zip(request.timer_tag_name[offset:to], request.timer_tag_value[offset:to]):
                        tags[str(request.dictionary[tag_name])] = str(request.dictionary[tag_value])
                    
                    timers.append((tags, (hit_count, timer_value)))
                    offset = to
            requests.append((
                (str(request.hostname), str(request.server_name), str(request.script_name)), 
                (request.document_size, request.request_time), 
                timers
            ))
        return requests

    def group(self, rows):
        """
        Group requests for 1 second, calc average time
        """
        requests = []
        for key, request in groupby(rows, key=lambda r: '#'.join(r[0])):
            tags = []
            for tag_key, tag in groupby(list(itertools.chain.from_iterable([r[2] for r in request])), key=lambda x: 'tag:%s:tag' % str(x[0])):
                rps = sum([x[1][0] for x in tag])
                tags.append((tag[0][0], rps, aggregate([x[1][1] for x in tag], rps)))
            requests.append((request[0][0], (len(request), sum([r[1][0] for r in request]), aggregate([r[1][1] for r in request])), tags))
        return requests


"""
    Pinba Daemon - starts UDP server on port 30002, recives packets from php, every second sends them to decoder, and 
    then sends them in usable format via zmq socket.
"""
class PinbaDaemon(object):
    def __init__(self):
        self.requests = []
        self.queue = JoinableQueue()
        self.is_running = False
        self.pub = None
        self.req = None

    # this handler will be run for each incoming connection in a dedicated greenlet
    def recv(self, msg, address):
        self.requests.append(msg)
        
    # every second collect requests from self.requests and send them to processing
    def interval(self):
        t = time.time()
        gevent.sleep(int(t + 1) - time.time())
        while self.is_running:
            t = time.time()
            requests = self.requests
            self.requests = []
            self.queue.put((int(t), requests), block=False)
            #print t, len(requests)
            self.counter = 0
            gevent.sleep(1 - (time.time() - t))

    def decoder(self):
        import simplejson as json
        try:
            while self.is_running:
                self.req.send_pyobj(self.queue.get())
                t, requests = self.req.recv_pyobj()
                #print 'decoder thread reply', t, len(requests)
                self.pub.send(json.dumps( (t, requests) ))
        except KeyboardInterrupt:            
            pass
        except Exception, e:
            print "PinbaDaemon::decoder got an exception"

    def run(self):
        self.is_running = True
        
        decoder = Decoder(os.getpid())
        decoder.start()
        
        # wait for it
        time.sleep(.5)

        context = gzmq.Context()
        
        self.pub = context.socket(gzmq.PUB)
        self.pub.bind('tcp://*:5000')
        self.pub.setsockopt(gzmq.HWM, 60)
        self.pub.setsockopt(gzmq.SWAP, 25000000)

        self.req = context.socket(gzmq.REQ)
        self.req.connect('tcp://127.0.01:5042')

        pool = Pool(5000)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind(('0.0.0.0', 30002))
        
        server = DgramServer(udp_socket, self.recv, spawn=pool)
        print "Starting udp server on port 30002"
        try:    
            workers = [gevent.spawn(self.interval), gevent.spawn_later(1, self.decoder)]
            server.serve_forever()
        except KeyboardInterrupt:            
            pass
        except Exception, e:
            print "PinbaDaemon got an exception"
        
        self.is_running = False
        gevent.joinall(workers)
        self.queue.join()
        self.pub.close()
        context.term()
        decoder.terminate()

"""
    UDP Server for gevent.
    Based on http://code.google.com/p/gevent/issues/detail?id=50
"""

# Copyright (c) 2009-2010 Denis Bilenko. See LICENSE for details.
"""UDP/SSL server"""
class DgramServer(BaseServer):
    """A generic UDP server. Receive UDP package on a listening socket and spawns user-provided *handle*
    for each connection with 2 arguments: the client message and the client address.

    Note that although the errors in a successfully spawned handler will not affect the server or other connections,
    the errors raised by :func:`accept` and *spawn* cause the server to stop accepting for a short amount of time. The
    exact period depends on the values of :attr:`min_delay` and :attr:`max_delay` attributes.

    The delay starts with :attr:`min_delay` and doubles with each successive error until it reaches :attr:`max_delay`.
    A successful :func:`accept` resets the delay to :attr:`min_delay` again.
    """

    # the number of seconds to sleep in case there was an error in recefrom() call
    # for consecutive errors the delay will double until it reaches max_delay
    # when accept() finally succeeds the delay will be reset to min_delay again
    min_delay = 0.01
    max_delay = 1

    def __init__(self, listener, handle=None, backlog=None, spawn='default', **ssl_args):
        BaseServer.__init__(self, listener, handle=handle, backlog=backlog, spawn=spawn)
        self.delay = self.min_delay
        self._recv_event = None
        self._start_receving_timer = None

    def set_listener(self, listener, backlog=None):
        BaseServer.set_listener(self, listener, backlog=backlog)
        try:
            self.socket = self.socket._sock
        except AttributeError:
            pass

    def set_spawn(self, spawn):
        BaseServer.set_spawn(self, spawn)
        if self.pool is not None:
            self.pool._semaphore.rawlink(self._start_receiving)

    def set_handle(self, handle):
        BaseServer.set_handle(self, handle)
        self._handle = self.handle

    #@property
    #def started(self):
    #    return self._recv_event is not None or self._start_receving_timer is not None

    def start_accepting(self):
        if self._recv_event is None:
            self._recv_event = core.read_event(self.socket.fileno(), self._do_recv, persist=True)

    def _start_receiving(self, _event):
        if self._recv_event is None:
            if 'socket' not in self.__dict__:
                return
            self._recv_event = core.read_event(self.socket.fileno(), self._do_recv, persist=True)

    def stop_accepting(self):
        if self._recv_event is not None:
            self._recv_event.cancel()
            self._recv_event = None
        if self._start_receving_timer is not None:
            self._start_receving_timer.cancel()
            self._start_receving_timer = None

    def _do_recv(self, event, _evtype):
        assert event is self._recv_event
        address = None
        try:
            if self.full():
                self.stop_accepting()
                return
            try:
                msg, address = self.socket.recvfrom(1024)
            except socket.error, err:
                if err[0]==errno.EAGAIN:
                    sys.exc_clear()
                    return
                raise

            self.delay = self.min_delay
            spawn = self._spawn
            if spawn is None:
                self._handle(msg, address)
            else:
                spawn(self._handle, msg, address)
            return
        except:
            traceback.print_exc()
            ex = sys.exc_info()[1]
            if self.is_fatal_error(ex):
                self.kill()
                sys.stderr.write('ERROR: %s failed with %s\n' % (self, str(ex) or repr(ex)))
                return
        try:
            if address is None:
                sys.stderr.write('%s: Failed.\n' % (self, ))
            else:
                sys.stderr.write('%s: Failed to handle request from %s\n' % (self, address, ))
        except Exception:
            traceback.print_exc()
        if self.delay >= 0:
            self.stop_accepting()
            self._start_receving_timer = core.timer(self.delay, self.start_accepting)
            self.delay = min(self.max_delay, self.delay*2)
        sys.exc_clear()

    def is_fatal_error(self, ex):
        return isinstance(ex, socket.error) and ex[0] in (errno.EBADF, errno.EINVAL, errno.ENOTSOCK)

if __name__ == "__main__":
    daemon = PinbaDaemon()
    try:
        daemon.run()
    except KeyboardInterrupt:
        print "\nGot Ctrl-C, shutting down..."
    except Exception, e:
        print "Oops...", e