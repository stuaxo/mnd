Match 'n Dispatch
=================

Match python args and dispatch based on their contents.


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

Install
-------

```$ pip install mnd```


Unit Test
---------

```$ python setup.py test```




[![Build status][ci-image]][ci-url]
[ci-image]: https://travis-ci.org/stuaxo/mnd.png?branch=master
[ci-url]: https://travis-ci.org/stuaxo/mnd
