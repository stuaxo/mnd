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

Use the handy decorator
```python
>>> @handler(d, msg="hello")
>>> def say(msg=None):
...     print "got message: ", msg
```

Try dispatching some events
```python
>>> d.dispatch(msg="gets filtered out..."))
>>> d.dispatch(msg="hello"))
got message: hello
```

Install
-------

```$ pip install mnd```
