PINBA TO ZMQ
=================

DRAFT!

Python daemon for collection and basic aggregation of pinba (http://pinba.org) data.

Use: gevent, pyzmq, gevent_zmq, protobuf, simplejson

Демон на питоне для начального сбора и агрегации данных от пинбы (http://pinba.org).

Использует: gevent, pyzmq, gevent_zmq, protobuf, simplejson

+ http://www.gevent.org/
+ http://www.zeromq.org/bindings:python
+ https://github.com/traviscline/gevent-zeromq
+ https://github.com/simplejson/simplejson
+ http://code.google.com/p/protobuf/
+ https://github.com/Greplin/fast-python-pb

How to use / Как использовать:
-----

Install/compile all from links above, from folder pinba_pb install wrapper for protobuf packet.
Then just start daemon.py and it should start listning port 30002 for pinba packets and port 5000 as zeromq.pub socket for results. Results it sends in JSON format.

Всё вышеперечисленное установить/скомпилировать, из папки pinba_pb поставить обётку для protobuf-сообщений пинбы.
Потом просто запускаем daemon.py и он должен начать слушать порт 30002 для пакетов от пинбы и порт 5000 как zmq.pub сокет.
Туда он отдает в формате json время плюс массив с данными запросов.

Format of results / Формат следующий:

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

Time in folowing format / Время идёт в формате:

``` js
{
	'med': медиана / median, 
	'p75': 75% пеценталь / percentile, 
	'max': максимум / maximum, 
	'dev': среднеквадратичное отклонение / stddev, 
	'p85': 85% перценталь / percentile, 
	'avg': среднее / average
}
```

All time values is in microseconds.

It primary usage is for real-time monitoring or analisys of php.

Всё в микросекундах.

Эти данные потом можно или записывать в какое-либо хранилище или использовать для любого анализа в реальном времени.

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