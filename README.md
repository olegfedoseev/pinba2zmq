PINBA TO ZMQ
=================

DRAFT!

Демон на питоне для начального сбора и агрегации данных от пинбы.
Использует: gevent, pyzmq, gevent_zmq, protobuf, simplejson

+ http://www.gevent.org/
+ http://www.zeromq.org/bindings:python
+ https://github.com/traviscline/gevent-zeromq
+ https://github.com/simplejson/simplejson
+ http://code.google.com/p/protobuf/
+ https://github.com/Greplin/fast-python-pb

Как использовать:
-----

Всё вышеперечисленное установить/скомпилировать, из папки pinba_pb поставить обётку для protobuf-сообщений пинбы.
Потом просто запускаем daemon.py и он должен начать слушать порт 30002 для пакетов от пинбы и порт 5000 как zmq.pub сокет.
Туда он отдает в формате json время плюс массив с данными запросов.
Формат следующий:

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

Время идёт в формате:

``` js
{
	'med': медиана, 
	'p75': 75% пеценталь, 
	'max': максимум, 
	'dev': среднеквадратичное отклонение, 
	'p85': 85% перценталь, 
	'avg': среднее
}
```

Всё в микросекундах

Эти данные потом можно или записывать в какое-либо хранилище или использовать для любого анализа в реальном времени.

Автор
-------

**Олег Федосеев**

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