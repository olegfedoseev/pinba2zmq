PINBA TO ZMQ
=================

DRAFT!

Python daemon for collection and basic aggregation of pinba (http://pinba.org) data.

Use: gevent, pyzmq, gevent_zmq, protobuf, simplejson

+ http://www.gevent.org/
+ http://www.zeromq.org/bindings:python
+ https://github.com/traviscline/gevent-zeromq
+ https://github.com/simplejson/simplejson
+ http://code.google.com/p/protobuf/
+ https://github.com/Greplin/fast-python-pb
+ http://pypi.python.org/pypi/python-daemon/

How to use
-----

Install/compile all from links above, from folder pinba_pb install wrapper for protobuf packet.
Start script in debug mode, in foreground like that:

``` shell
> python daemon.py [--log /path/to/file.log] [--pid /path/to/file.pid]
```

By default it use path /var/log/pinba.log for log file and /var/run/pinba.pid for PID file.

To start in production mode, as daemon just add -d option:

``` shell
> python daemon.py -d [--log /path/to/file.log] [--pid /path/to/file.pid]
```

To stop daemon add "stop":

``` shell
> python daemon.py -d [--log /path/to/file.log] [--pid /path/to/file.pid] stop
```

You can also specify ip (-i|--ip 0.0.0.0), port (-p|--port 30002) and address for output socket (--out "tcp://*:5000")

After start it should start listning port 30002 for pinba packets and port 5000 as zeromq.pub socket for results. Results it sends in JSON format.

Format of results:

``` js
[
	['host', 'server', 'script'],
	[rps, doc_size, {'med': 14786, 'p75': 14786, 'max': 14786, 'dev': 14786, 'p85': 14786, 'avg': 14786}], 
	[
		[{'tag_name': 'tag_value', ...}, rps, {'med': 422, 'p75': 422, 'max': 422, 'dev': 422, 'p85': 422, 'avg': 422}], 
		...
	],
	...
]
```

Time is in folowing format:

``` js
{
	'med': median, 
	'p75': 75% percentile, 
	'max': maximum, 
	'dev': stddev, 
	'p85': 85% percentile, 
	'avg': average
}
```

All time values is in microseconds.

It primary usage is for real-time monitoring or analisys of php.

Author
-------

**Oleg Fedoseev**

+ http://twitter.com/olegfedoseev
+ http://github.com/aryoh

Copyright and license
---------------------

Copyright 2011 Oleg Fedoseev

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this work except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at:

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.