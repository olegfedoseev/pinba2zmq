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

import time
import zlib
import traceback
import logging
import logging.handlers
from optparse import OptionParser

import gevent
from gevent import Timeout, socket
from gevent.monkey import patch_all
from gevent.pool import Pool

from gevent_zeromq import zmq
from dgramserver import DgramServer

logger = logging.getLogger("pinba")
patch_all()


class PinbaToZmq(object):
    """
        Pinba Daemon - starts UDP server on port 30002, recives packets from php, every second sends them to decoder, and
        then sends them in usable format via zmq socket.
    """
    def __init__(self):
        self.workers = []
        self.requests = []
        self.req = None
        self.pub = None

    def recv(self, msg, address):
        # this handler will be run for each incoming connection in a dedicated greenlet
        self.requests.append(msg)

    def interval(self):
        # every second collect requests from self.requests and send them to processing
        gevent.spawn_later(1, self.interval)
        requests = self.requests
        ts = int(time.time())
        self.requests = []

        data = zlib.compress('\n--\n'.join(requests))
        self.pub.send("%s\n%s" % (ts, data))
        logger.info("[%d] Send %d bytes and %d requests" % (ts, len(data), len(requests)))

    def run(self, in_addr="0.0.0.0:30002", out_addr="tcp://*:5000"):
        ip, port = in_addr.split(':')

        logger.info("Listen on %s:%s, output goes to: %s" % (ip, port, out_addr))
        context = zmq.Context()

        self.pub = context.socket(zmq.PUB)
        self.pub.bind(out_addr)
        self.pub.setsockopt(zmq.HWM, 1)
        self.pub.setsockopt(zmq.SWAP, 512 * 1024 * 1024)

        pool = Pool(5000)
        self.server = DgramServer(ip, int(port), self.recv, spawn=pool)
        logger.info("Ready!")
        try:
            self.workers = [gevent.spawn_later(1, self.interval)]
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception:
            logger.error(traceback.format_exc())

        logger.info("Daemon shutting down")
        if self.pub:
            self.pub.close()
        gevent.killall(self.workers)
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
