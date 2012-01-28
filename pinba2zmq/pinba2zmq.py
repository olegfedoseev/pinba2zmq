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

import os
import time
import multiprocessing
import itertools
import math
import traceback
import signal
import logging
import logging.handlers
from optparse import OptionParser

import gevent
from gevent import Timeout
from gevent.monkey import patch_all
from gevent.pool import Pool

import ujson
from gevent_zeromq import zmq

# protobuf message
from Pinba import Request
from dgramserver import DgramServer

logger = logging.getLogger("pinba")
patch_all()


class groupby(dict):
    def __init__(self, seq, key=lambda x: x):
        for value in seq:
            self.setdefault(key(value), []).append(value)
    __iter__ = dict.iteritems


class Decoder(multiprocessing.Process):
    """
    Process that receives ProtoBuf encoded messages from Pinba, decodes it and group it by host+server+script[+tags]
    """
    def __init__(self, pid, out_addr):
        multiprocessing.Process.__init__(self)
        self.parent = pid
        self.out_addr = out_addr

    def avg(self, values, cnt=None):
        return float(sum(map(float, values)) / (len(values) if cnt is None else cnt))

    def stddev(self, values, cnt=None):
        return float((sum((v - self.avg(values)) ** 2 for v in values) / (len(values) if cnt is None else cnt)) ** 0.5)

    def median(self, values):
        return float(sorted(values)[len(values) / 2])

    def percentile(self, values, percentile=75):
        idx = math.trunc(((100 - percentile) / 100) * len(values))
        if idx > 0:
            values = sorted(values)[idx:]
        return float(sum(values) / len(values))

    def aggregate(self, values, cnt=None):
        if cnt is None:
            cnt = len(values)

        if cnt == 0:
            return {'max': 0, 'p85': 0, 'avg': 0, 'med': 0, 'dev': 0}
        if cnt == 1:
            val = values[0]
            return {'max': val, 'p85': val, 'avg': val, 'med': val, 'dev': val}

        return {
            'max': max(values),
            'p85': self.percentile(values, 85),
            'avg': self.avg(values, cnt),
            'med': self.median(values),
            'dev': self.stddev(values, cnt),
        }

    def run(self):
        context = zmq.Context()

        incoming = context.socket(zmq.PULL)
        incoming.bind("ipc:///tmp/pinba2zmq.sock")

        pub = context.socket(zmq.PUB)
        pub.bind(self.out_addr)
        pub.setsockopt(zmq.HWM, 1)
        pub.setsockopt(zmq.SWAP, 512 * 1024 * 1024)

        logger.info("%s ready" % multiprocessing.current_process().name)
        try:
            while os.getppid() == self.parent:
                t = None
                with Timeout(5, False):
                    t, raw_requests = incoming.recv_pyobj()
                    pub.send(ujson.encode((t, self.group(self.decode(raw_requests)))))
                if not t:
                    logger.info("Timeout!")
        except (zmq.ZMQError, KeyboardInterrupt):
            pass
        except Exception:
            logger.info("%s get exception" % multiprocessing.current_process().name)
            logger.error(traceback.format_exc())

        logger.info("Decoder process stops")
        incoming.close()
        pub.close()
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
                    request_timers = zip(request.timer_tag_count, request.timer_hit_count, request.timer_value)
                    for tag_count, hit_count, timer_value in request_timers:
                        tags = {}
                        to = offset + tag_count
                        timer_tags = zip(request.timer_tag_name[offset:to], request.timer_tag_value[offset:to])
                        for tag_name, tag_value in timer_tags:
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
        return requests

    def group(self, rows):
        """
        Group requests for 1 second, calc average time
        """
        result = []
        try:
            for key, request in groupby(rows, key=lambda r: '#'.join([str(v) for v in r[0]])):
                tags = []
                requests = list(itertools.chain.from_iterable([r[2] for r in request]))
                request_tags = groupby(requests, key=lambda x: 'tag:%s:tag' % str(x[0]))
                for tag_key, tag in request_tags:
                    rps = sum([int(x[1][0]) for x in tag])
                    tags.append((tag[0][0], rps, self.aggregate([x[1][1] for x in tag], rps)))
                try:
                    result.append((
                        request[0][0],                                          # request "id" - host, server, script
                        (len(request), sum([int(r[1][0]) for r in request]),    # rps
                        self.aggregate([float(r[1][1]) for r in request])),     # size
                        tags                                                    # timers
                    ))
                except:
                    pass
        except UnicodeEncodeError:
            logger.debug("Got UnicodeEncodeError Exception!")
        return result


class PinbaToZmq(object):
    """
        Pinba Daemon - starts UDP server on port 30002, recives packets from php, every second sends them to decoder, and
        then sends them in usable format via zmq socket.
    """
    def __init__(self):
        self.requests = []
        self.is_running = False
        self.pub = None
        self.req = None

    def recv(self, msg, address):
        # this handler will be run for each incoming connection in a dedicated greenlet
        self.requests.append(msg)

    def interval(self):
        # every second collect requests from self.requests and send them to processing
        if self.is_running:
            gevent.spawn_later(1, self.interval)
        self.push.send_pyobj((int(time.time()), self.requests))
        self.requests = []

    def stop(self, signum=None, frame=None):
        self.is_running = False

    def watcher(self):
        try:
            while self.is_running:
                gevent.sleep(1)
            logger.info("Try to stop server...")
            self.server.stop()
        except Exception:
            logger.error(traceback.format_exc())
        logger.info("Watcher thread stops")

    def run(self, in_addr="0.0.0.0:30002", out_addr="tcp://*:5000"):
        self.is_running = True
        signal.signal(signal.SIGTERM, self.stop)
        ip, port = in_addr.split(':')

        self.child = Decoder(os.getpid(), out_addr)
        self.child.start()
        time.sleep(.5)

        logger.info("Listen on %s:%s, output goes to: %s" % (ip, port, out_addr))
        context = zmq.Context()
        self.push = context.socket(zmq.PUSH)
        self.push.connect("ipc:///tmp/pinba2zmq.sock")

        pool = Pool(5000)
        self.server = DgramServer(ip, int(port), self.recv, spawn=pool)
        logger.info("Ready!")
        try:
            gevent.spawn(self.watcher)
            self.workers = [gevent.spawn_later(1, self.interval)]
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception:
            logger.error(traceback.format_exc())

        logger.info("Daemon shutting down")
        self.is_running = False
        gevent.killall(self.workers)
        self.pub.close()
        self.child.terminate()
        logger.info("Daemon stops")


def main():
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", help="verbose output", action="store_true", default=False)
    parser.add_option("-p", "--pinba", dest="pinba", help="ip and port to listen", type="string", default="0.0.0.0:30002")
    parser.add_option("-o", "--out", dest="out", help="output address for zmq", type="string", default="tcp://*:5000")
    parser.add_option("-l", "--log", dest="log", help="log file path", type="string", default="/var/log/pinba.log")
    (options, args) = parser.parse_args()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh = logging.FileHandler(options.log)
    ch = logging.StreamHandler()

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.setLevel(logging.DEBUG if options.verbose else logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(ch)

    pinba2zmq = PinbaToZmq()
    logger.info("Starting pinba2zmq...")
    try:
        pinba2zmq.run(options.pinba or '0.0.0.0:30002', options.out or 'tcp://*:5000')
    except KeyboardInterrupt:
        pinba2zmq.stop()

if __name__ == "__main__":
    main()
