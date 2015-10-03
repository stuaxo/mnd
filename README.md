Match 'n Dispatch
=================

Match python args and dispatch based on their contents.


Getting started
---------------

Create a dispatcher
>>> d = Dispatcher()


Use the handy decorator
>>> @handler(d, blah=1)
>>> def blah(blah=None):
...     print "got blah: ", blah


Try dispatching some events
>>> d.dispatch(blah(blah=2))
>>> d.dispatch(blah(blah=1))
got blah: 1


Install
-------

```$ pip install mnd```
