Pinba to ZeroMQ
=================

Python daemon for collection and basic aggregation of Pinba (http://pinba.org) data.


About
-----
Production ready. It used 24/7 with load around 5000rps on small VPS.
We use data from it to build real-time graphs. (Hope to open-source it to in near future)

How to use
-----

First of all you need to install ProtoBuf from http://code.google.com/p/protobuf/ and fast-python-pb from https://github.com/Greplin/fast-python-pb

After that you need just clone repo:

``` shell
git clone https://github.com/aryoh/pinba2zmq.git
cd pinba2zmq
python setup.py install
```

Now, if you want pinba2zmq to start with your server (if you on Ubuntu):
``` shell
sudo chmod +x /etc/init.d/pinba2zmq && sudo update-rc.d pinba2zmq defaults
````

And to start:
``` shell
sudo service pinba2zmq start
```

Command line arguments
-----

When you start pinba2zmq, you can use following arguments:
``` shell
pinba2zmq [-l|--log /path/to/file.log] [-v|--verbose] [-p|--pinba 0.0.0.0:30002] [-o|--out tcp://*:5000]
```

After start it should start listning port 30002 for pinba packets and port 5000 as zeromq.pub socket for results. Results it sends in JSON format.

Format of results:

``` js
[
	['host', 'server', 'script'],
	[rps, doc_size, {'med': 14786, 'max': 14786, 'dev': 14786, 'p85': 14786, 'avg': 14786}], 
	[
		[{'tag_name': 'tag_value', ...}, rps, {'med': 422, 'max': 422, 'dev': 422, 'p85': 422, 'avg': 422}], 
		...
	],
	...
]
```

Time is in folowing format:

``` js
{
	'avg': average
	'med': median, 
	'max': maximum, 
	'dev': stddev, 
	'p85': 85% percentile, 
}
```

All time values is in microseconds.


Dependencies
------
gevent, pyzmq, gevent_zmq, protobuf, simplejson

+ http://www.gevent.org/
+ http://www.zeromq.org/bindings:python
+ https://github.com/traviscline/gevent-zeromq
+ https://github.com/simplejson/simplejson
+ http://code.google.com/p/protobuf/
+ https://github.com/Greplin/fast-python-pb
+ http://pypi.python.org/pypi/python-daemon/


Author
-------

**Oleg Fedoseev**

+ http://twitter.com/olegfedoseev
+ http://github.com/aryoh

Copyright and license
---------------------

Copyright 2011-2012 Oleg Fedoseev

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this work except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at:

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.