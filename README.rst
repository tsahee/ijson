.. image:: https://travis-ci.com/ICRAR/ijson.svg?branch=master
    :target: https://travis-ci.com/ICRAR/ijson

.. image:: https://coveralls.io/repos/github/ICRAR/ijson/badge.svg?branch=master
    :target: https://coveralls.io/github/ICRAR/ijson?branch=master

.. image:: https://badge.fury.io/py/ijson.svg
    :target: https://badge.fury.io/py/ijson

.. image:: https://img.shields.io/pypi/pyversions/ijson.svg
    :target: https://pypi.python.org/pypi/ijson

.. image:: https://img.shields.io/pypi/dd/ijson.svg
    :target: https://pypi.python.org/pypi/ijson

.. image:: https://img.shields.io/pypi/dw/ijson.svg
    :target: https://pypi.python.org/pypi/ijson

.. image:: https://img.shields.io/pypi/dm/ijson.svg
    :target: https://pypi.python.org/pypi/ijson


=====
ijson
=====

Ijson is an iterative JSON parser with a standard Python iterator interfaces.


Usage
=====

All usage example will be using a JSON document describing geographical
objects:

.. code-block:: json

    {
      "earth": {
        "europe": [
          {"name": "Paris", "type": "city", "info": { ... }},
          {"name": "Thames", "type": "river", "info": { ... }},
          // ...
        ],
        "america": [
          {"name": "Texas", "type": "state", "info": { ... }},
          // ...
        ]
      }
    }


High-level interfaces
---------------------

Most common usage is having ijson yield native Python objects out of a JSON
stream located under a prefix. Here's how to process all European cities:

.. code-block::  python

    import ijson

    f = urlopen('http://.../')
    objects = ijson.items(f, 'earth.europe.item')
    cities = (o for o in objects if o['type'] == 'city')
    for city in cities:
        do_something_with(city)

For how to build a prefix see the Prefix section below.

Other times it might be useful to iterate over object members
rather than objects themselves (e.g., when objects are too big).
In that case one can use the ``kvitems`` functions instead:

.. code-block::  python

    import ijson

    f = urlopen('http://.../')
    european_places = ijson.kvitems(f, 'earth.europe.item')
    names = (v for k, v in european_places if k == 'name')
    for name in names:
        do_something_with(name)


Lower-level interfaces
----------------------

Sometimes when dealing with a particularly large JSON payload it may worth to
not even construct individual Python objects and react on individual events
immediately producing some result:

.. code-block::  python

    import ijson

    parser = ijson.parse(urlopen('http://.../'))
    stream.write('<geo>')
    for prefix, event, value in parser:
        if (prefix, event) == ('earth', 'map_key'):
            stream.write('<%s>' % value)
            continent = value
        elif prefix.endswith('.name'):
            stream.write('<object name="%s"/>' % value)
        elif (prefix, event) == ('earth.%s' % continent, 'end_map'):
            stream.write('</%s>' % continent)
    stream.write('</geo>')

Even more bare-bones is the ability to react on individual events
without even calculating a prefix:

.. code-block:: python

    import ijson

    events = ijson.basic_parse(urlopen('http://.../'))
    num_names = sum(1 for event, value in events
                    if event == 'map_key' and value == 'name')


``asyncio`` support
-------------------

In python 3.5+ all of the methods above
have an ``*_async`` counterpart
that works on file-like asynchronous objects,
and that can be iterated asynchronously.
In other words, something like this:

.. code-block:: python

   import asyncio
   import ijson

   async def run():
      f = await async_urlopen('http://..../')
      async for object in ijson.items_async(f, 'earth.europe.item'):
         if object['type'] == 'city':
            do_something_with(city)
   asyncio.run(run())


Push interfaces
---------------

All examples above use a file-like object as the data input
(both the normal case, and for ``asyncio`` support),
and hence are "pull" interfaces,
with the library reading data as necessary.
If for whatever reason it's not possible to use such method,
you can still **push** data
through yet a different interface: coroutines.
Coroutines effectively allow users
to send data to them at any point in time,
with a final *target* coroutine-like object
receiving the results.

In the following example
the user is doing the reading
instead of letting the library do it:

.. code-block:: python

   import ijson

   @ijson.coroutine
   def print_cities():
      while True:
         obj = (yield)
         if obj['type'] != 'city':
            continue
         print(obj)

   coro = ijson.items_coro(print_cities(), 'earth.europe.item')
   f = urlopen('http://.../')
   chunk = f.read(buf_size)
   while chunk:
      try:
         coro.send(chunk)
      except StopIteration:
            break
      chunk = f.read()

All four ijson iterators
have a ``*_coro`` counterpart
that work by pushing data into them.
Instead of receiving a file-like object
and option buffer size as arguments,
they receive a single ``target`` argument,
which should be a coroutine-like object
(anything implementing a ``send`` method)
through which results will be published.


Events
======

When using the lower-level ``ijson.parse`` function,
three-element tuples are generated
containing a prefix, an event name, and a value.
Events will be one of the following:

- ``start_map`` and ``end_map`` indicate
  the beginning and end of a JSON object, respectively.
  They carry a ``None`` as their value.
- ``start_array`` and ``end_array`` indicate
  the beginning and end of a JSON array, respectively.
  They also carry a ``None`` as their value.
- ``map_key`` indicates the name of a field in a JSON object.
  Its associated value is the name itself.
- ``null``, ``boolean``, ``integer``, ``double``, ``number`` and ``string``
  all indicate actual content, which is stored in the associated value.


Prefix
======

A prefix represents the context within a JSON document
where an event originates at.
It works as follows:

- It starts as an empty string.
- A ``<name>`` part is appended when the parser starts parsing the contents
  of a JSON object member called ``name``,
  and removed once the content finishes.
- A literal ``item`` part is appended when the parser is parsing
  elements of a JSON array,
  and removed when the array ends.
- Parts are separated by ``.``.

When using the ``ijson.items`` function,
the prefix works as the selection
for which objects should be automatically built and returned by ijson.


Backends
========

Ijson provides several implementations of the actual parsing in the form of
backends located in ijson/backends:

- ``yajl2_c``: a C extension using `YAJL <http://lloyd.github.com/yajl/>`_ 2.x.
  This is the fastest, but *might* require a compiler and the YAJL development files
  to be present when installing this package.
  Binary wheel distributions exist for major platforms/architectures to spare users
  from having to compile the package.
- ``yajl2_cffi``: wrapper around `YAJL <http://lloyd.github.com/yajl/>`_ 2.x
  using CFFI.
- ``yajl2``: wrapper around YAJL 2.x using ctypes, for when you can't use CFFI
  for some reason.
- ``yajl``: deprecated YAJL 1.x + ctypes wrapper, for even older systems.
- ``python``: pure Python parser, good to use with PyPy

You can import a specific backend and use it in the same way as the top level
library:

.. code-block::  python

    import ijson.backends.yajl2_cffi as ijson

    for item in ijson.items(...):
        # ...

Importing the top level library as ``import ijson``
uses the first available backend in the same order of the list above.


Acknowledgements
================

ijson was originally developed and actively maintained until 2016
by `Ivan Sagalaev <http://softwaremaniacs.org/>`_.
In 2019 he
`handed over <https://github.com/isagalaev/ijson/pull/58#issuecomment-500596815>`_
the maintenance of the project and the PyPI ownership.

Python parser in ijson is relatively simple thanks to `Douglas Crockford
<http://www.crockford.com/>`_ who invented a strict, easy to parse syntax.

The `YAJL <http://lloyd.github.com/yajl/>`_ library by `Lloyd Hilaiel
<http://lloyd.io/>`_ is the most popular and efficient way to parse JSON in an
iterative fashion.

Ijson was inspired by `yajl-py <http://pykler.github.com/yajl-py/>`_ wrapper by
`Hatem Nassrat <http://www.nassrat.ca/>`_. Though ijson borrows almost nothing
from the actual yajl-py code it was used as an example of integration with yajl
using ctypes.
