Match 'n Dispatch
=================

Match python args and dispatch based on their contents.


Install
-------

```$ pip install mnd```


Getting started
---------------

Create a dispatcher
```python
from mnd.dispatch import Dispatcher, handle

>>> d = Dispatcher()
```

Add a handler with the handy decorator
```python
>>> @handler(d, msg="hello")
>>> def say(msg=None):
...     print "got message: ", msg
```

Try dispatching some events
```python
>>> d.dispatch(msg="gets filtered out...")
>>> d.dispatch(msg="hello")
got message: hello
```


Filter using 'in'
-----------------

```python
>>> @handler(d, msg__in=["hello", "hi"])
>>> def greeting(msg=None):
...     print "greetings"
>>> d.dispatch(msg="hello")
greetings
>>> d.dispatch(msg="hi")
greetings
```

As well as __in, operations lt, le, eq, ne, ge, gt are supported


Filter by attribute
-------------------


```python
from collections import namedtuple
Worm=namedtuple("Worm", "segments")
worm1=Worm(4)
worm2=Worm(100)
>>> @handler(d, dict(segments__gt=50))
>>> def long_worm(w):
...     print "long worm with %s segment.s" % segments)
>>> d.dispatch(worm1)
>>> d.dispatch(worm2)
long worm with 100 segments.
```




Unit Test
---------

```$ python setup.py test```




[![Build status][ci-image]][ci-url]
[ci-image]: https://travis-ci.org/stuaxo/mnd.png?branch=master
[ci-url]: https://travis-ci.org/stuaxo/mnd
