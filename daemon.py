#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Oleg Fedoseev <oleg.fedoseev@me.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import with_statement

import os, sys, time, multiprocessing, itertools, math, errno, traceback, signal, resource
from optparse import OptionParser
import sys, logging, logging.handlers, traceback

import gevent
from gevent.monkey import patch_all; patch_all()
from gevent.queue import JoinableQueue
from gevent.pool import Pool
from gevent.baseserver import BaseServer
from gevent import socket, core

import simplejson as json
from gevent_zeromq import zmq as gzmq
import daemon
import daemon.pidlockfile

from Pinba import Request

logger = logging.getLogger("pinba")

class groupby(dict):
    def __init__(self, seq, key=lambda x:x):
        for value in seq:
            self.setdefault(key(value), []).append(value)
    __iter__ = dict.iteritems

class Decoder(multiprocessing.Process):
    def __init__(self, pid):
        multiprocessing.Process.__init__(self)
        self.parent = pid

    def avg(self, values, cnt=None):
        return sum(map(float, values)) / (len(values) if cnt is None else cnt)

    def stddev(self, values, cnt=None):
        mean = self.avg(values)
        return (sum((v - mean) ** 2 for v in values) / (len(values) if cnt is None else cnt)) ** 0.5

    def median(self, values):
        """
        A median is also known as the 50th percentile. Exactly 50% of people make less than the median and 50% make more.
        """
        return sorted(values)[len(values) / 2]

    def percentile(self, values, percentile=75):
        idx = math.trunc(((100 - percentile) / 100) * len(values))
        if idx > 0:
            values = sorted(values)[idx:]
        return sum(values) / len(values)

    def aggregate(self, values, cnt=None):
        if cnt is None:
            cnt = len(values)

        if cnt == 0:
            return { 'max': 0, 'p75': 0, 'p85': 0, 'avg': 0, 'med': 0, 'dev': 0 }
        if cnt == 1:
            val = int(values[0] * 1000000)
            return { 'max': val, 'p75': val, 'p85': val, 'avg': val, 'med': val, 'dev': val }

        return {
            'max': int(max(values) * 1000000),
            'p75': int(self.percentile(values, 75) * 1000000),
            'p85': int(self.percentile(values, 85) * 1000000),
            'avg': int(self.avg(values, cnt) * 1000000),
            'med': int(self.median(values) * 1000000),
            'dev': int(self.stddev(values, cnt) * 1000000),
        }

    def run(self):
        import zmq
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:5042")
        logger.info("%s ready" % multiprocessing.current_process().name)
        try:
            while os.getppid() == self.parent:
                t, raw_requests = socket.recv_pyobj()
                socket.send_pyobj((t, self.group(self.decode(raw_requests))))
        except (zmq.ZMQError, KeyboardInterrupt):
            pass
        except Exception, e:
            logger.info("%s get exception" % multiprocessing.current_process().name)
            logger.error(traceback.format_exc())

        logger.info("Decoder stops")
        socket.close()
        context.term()

    def decode(self, rows):
        """
        Decode protobuf packets and format data in usable format

        Return data in format: [((host, server, script), (doc_size, req_time), [timers]), ...]
        """
        requests = []
        for r in rows:
            try:
                request = Request()
                request.ParseFromString(r)

                timers = []
                if len(request.timer_hit_count) > 0:
                    offset = 0
                    for tag_count, hit_count, timer_value in zip(request.timer_tag_count, request.timer_hit_count, request.timer_value):
                        tags = {}
                        to = offset + tag_count
                        for tag_name, tag_value in zip(request.timer_tag_name[offset:to], request.timer_tag_value[offset:to]):
                            tags[request.dictionary[tag_name]] = request.dictionary[tag_value]
                        timers.append((tags, (hit_count, timer_value)))
                        offset = to
                requests.append((
                    (request.hostname, request.server_name, request.script_name),
                    (request.document_size, request.request_time),
                    timers
                ))
            except UnicodeDecodeError:
                logger.info("Got UnicodeDecodeError Exception!")
            except Exception:
                logger.info("UnicodeDecodeError pass but there are Exception!")
                
        return requests

    def group(self, rows):
        """
        Group requests for 1 second, calc average time
        """
        result = []
        for key, request in groupby(rows, key=lambda r: '#'.join(r[0])):
            tags = []
            requests = list(itertools.chain.from_iterable([r[2] for r in request]))
            request_tags = groupby(requests, key=lambda x: 'tag:%s:tag' % str(x[0]))
            for tag_key, tag in request_tags:
                rps = sum([int(x[1][0]) for x in tag])
                tags.append((tag[0][0], rps, self.aggregate([x[1][1] for x in tag], rps)))

            result.append((request[0][0], (len(request), sum([int(r[1][0]) for r in request]), self.aggregate([float(r[1][1]) for r in request])), tags))
        return result

"""
    Pinba Daemon - starts UDP server on port 30002, recives packets from php, every second sends them to decoder, and
    then sends them in usable format via zmq socket.
"""
class PinbaDaemon(object):
    def __init__(self, ip="0.0.0.0", port=30002, out_addr="tcp://*:5000"):
        self.requests = []
        self.queue = JoinableQueue()
        self.is_running = False
        self.pub = None
        self.req = None
        self.ip = ip
        self.port = port
        self.out = out_addr

    def recv(self, msg, address):
        """
        this handler will be run for each incoming connection in a dedicated greenlet
        """
        self.requests.append(msg)

    def interval(self):
        """
        every second collect requests from self.requests and send them to processing
        """
        logger.info("Interval thread starts")
        t = time.time()
        gevent.sleep(int(t + 1) - time.time())
        try:
            while self.is_running:
                t = time.time()
                requests = self.requests
                self.requests = []
                self.queue.put((int(t), requests), block=False)
                self.counter = 0
                gevent.sleep(1 - (time.time() - t))
        except KeyboardInterrupt:
            pass
        logger.info("Interval thread stops")

    def decoder(self):
        try:
            while self.is_running:
                msg = None
                with gevent.Timeout(5, False):
                    self.req.send_pyobj(self.queue.get())
                    msg = self.req.recv_pyobj()
                if msg:
                    self.pub.send(json.dumps(msg))
                else:
                    logger.info("Decoder thread timeout")
        except (gzmq.ZMQError, KeyboardInterrupt):
            pass
        except Exception, e:
            logger.error(traceback.format_exc())
        logger.info("Decoder thread stops")

    def stop(self, signum=None, frame=None):
        self.is_running = False

    def watcher(self):
        try:
            while self.is_running:
                gevent.sleep(1)
            logger.info("Try to stop server...")
            self.server.stop()
        except Exception, e:
            logger.error(traceback.format_exc())
        logger.info("Watcher thread stops")

    def run(self):
        self.is_running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.child = Decoder(os.getpid())
        self.child.start()
        time.sleep(.5)

        logger.info("Listen on %s:%s, output goes to: %s" % (self.ip, self.port, self.out))
        context = gzmq.Context()
        self.pub = context.socket(gzmq.PUB)
        self.pub.bind(self.out)
        self.pub.setsockopt(gzmq.HWM, 60)
        self.pub.setsockopt(gzmq.SWAP, 25000000)
        self.req = context.socket(gzmq.REQ)
        self.req.connect("tcp://127.0.0.1:5042")

        pool = Pool(5000)
        self.server = DgramServer(self.ip, self.port, self.recv, spawn=pool)
        logger.info("Starting udp server on port 30002")
        try:
            gevent.spawn(self.watcher)
            self.workers = [gevent.spawn(self.interval), gevent.spawn_later(1, self.decoder)]
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception, e:
            logger.error(traceback.format_exc())

        logger.info("Daemon shutting down")
        self.is_running = False
        gevent.joinall(self.workers)
        self.pub.close()
        self.child.terminate()
        logger.info("Daemon stops")

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

    def __init__(self, host, port, handle=None, backlog=None, spawn='default', **ssl_args):
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        listener.bind((host, int(port)))

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

def run(options):
    daemon = PinbaDaemon(options.ip or '0.0.0.0', options.port or '30002', options.out or 'tcp://*:5000')
    try:
        logger.info("starting daemon..")
        daemon.run()
    except KeyboardInterrupt:
        daemon.stop()

def stop(options):
    print "Stopping daemon..."
    try:
        pf = file(options.pid, "r")
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        sys.stderr.write("pid_file at " + options.pid + " doesn't exist\n")
        return
    try:
        while 1:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.1)
    except OSError, err:
        err = str(err)
        if "No such process" in err:
            if os.path.exists(options.pid):
                os.remove(options.pid)
            print "OK"
        else:
            print str(err)
            sys.exit(1)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--daemon", dest="daemon", help="run as daemon", action="store_true", default=False)
    parser.add_option("-p", "--port", dest="port", help="which port to listen", type="int", default=30002)
    parser.add_option("-i", "--ip", dest="ip", help="which ip to listen", type="string", default="0.0.0.0")
    parser.add_option("-o", "--out", dest="out", help="output address for zmq", type="string", default="tcp://*:5000")
    parser.add_option("-l", "--log", dest="log", help="log file path", type="string", default="/var/log/pinba.log")
    parser.add_option("-P", "--pid", dest="pid", help="pid file path", type="string", default="/var/run/pinba.pid")
    (options, args) = parser.parse_args()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh = logging.FileHandler(options.log)
    ch = logging.StreamHandler()

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    #logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    pid = daemon.pidlockfile.TimeoutPIDLockFile(options.pid, 2)
    if options.daemon:
        if len(args) == 0:
            files = range(resource.getrlimit(resource.RLIMIT_NOFILE)[1] + 2)
            with daemon.DaemonContext(pidfile=pid, files_preserve=files, stdout=sys.stdout, stderr=sys.stderr, working_directory=os.getcwd()):
                logger.addHandler(fh)
                run(options)
        elif len(args) == 1 and args[0] == 'stop':
            sys.exit(stop(options))
    else:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ch)
        run(options)
