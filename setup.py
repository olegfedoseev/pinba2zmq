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

from setuptools import setup, Extension

setup(
    name='pinba2zmq',
    version='0.6b',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    url='https://github.com/aryoh/pinba2zmq',
    description="Daemon for collecting Pinba's (http://pinba.org) data.",
    long_description="Daemon for collecting Pinba's (http://pinba.org) data. It aggregate data by seconds and send it out via ZeroMQ socket",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Topic :: System :: Boot',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    author="Oleg Fedoseev",
    author_email="oleg.fedoseev@me.com",
    packages=['pinba2zmq'],
    install_requires=['gevent', 'gevent_zeromq'],
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': ['pinba2zmq = pinba2zmq.pinba2zmq:main']}
)
