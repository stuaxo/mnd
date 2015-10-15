"""
To make callbacks work with instance methods some things need to happen.

The handler decorator attaches instances of MNDInfo to functions to enable
the dispatcher to work with classes and instances via the Handler metaclass.

At instance creation time the metaclass converts finds any handlers with
MNDFunction, replaces them with MNDMethods + informs the dispatcher.
"""

import weakref

from collections import namedtuple


class MNDInfo(object):
    # base class
    def __init__(self, type):
        self.type = type
        
    @property
    def is_class(self):
        return self.type == "class"
    
    @property
    def is_function(self):
        return self.type == "function"
    
class MNDFunction(MNDInfo):
    """
    stores weakref to a function and list of weakrefs to
    dispatchers that point to it
    """
    def __init__(self, f):
        MNDInfo.__init__(self, "function")
        self._wf = weakref.ref(f)
        self.dispatchers = []
        
    @property
    def f(self):
        return self._wf()
    
    def unbind(self):
        # self.dispatcher.remove(self.f)
        pass

class MNDMethod(MNDInfo):
    def __init__(self, m):
        MNDInfo.__init__(self, "method")
        self._wm = weakref.ref(m)
        self.dispatchers = []
        
    @property
    def m(self):
        return self._wm()


        
class MNDClass(MNDInfo):
    def __init__(self, handlers):
        MNDInfo.__init__(self, "class")
        self.handlers = handlers
        self.members_bound = False
            


class Handler(type):
    """
    Metaclass enables instance methods to be used as handlers.
    """
    def __new__(meta, name, bases, dct):
        # find all decorated functions and store them in an MNDClass under __mnd__
        handlers = weakref.WeakValueDictionary()
        for mname, member in dct.items():
            mnd = getattr(member, "__mnd__", None)
            if mnd is not None and mnd.is_function:
                handlers[mname] = mnd

        dct['__mnd__'] = MNDClass(handlers)
        
        # wrap __init__
        wrapped_init = dct['__init__']
        def __init__(self, *args, **kwargs):
            # bind any decorated methods and 
            for name, mnd in self.__mnd__.handlers.items():
                if mnd.is_function:
                    f = mnd.f  # .f is a weakref - can be None
                    if f is None:
                        continue
                    
                    # swap knowledge of function for method
                    m = getattr(self, name)
                    if not m.__mnd__.is_function:
                        raise Exception("Method changed signature !")

                    # replace __mnd__
                    m.__dict__['__mnd__'] = MNDMethod(m)

                    # update dispatchers
                    for dispatcher in mnd.dispatchers:
                        dispatcher.replace_callback(f, m)

                    del(mnd)
            wrapped_init(self, *args, **kwargs)
            
        dct['__init__'] = __init__
        return super(Handler, meta).__new__(meta, name, bases, dct)
    def __init__(cls, name, bases, dct):
        super(Handler, cls).__init__(name, bases, dct)



def handle(dispatcher, *accept_args, **accept_kwargs):
    """
    :param dispatcher: dispatcher to recieve events from
    :param accept_args:   args to match on
    :param accept_kwargs: kwargs to match on
    Decorator to attach functions to dispatcher
    """
    def wrap(f):
        f.__mnd__ = MNDFunction(f)
        dispatcher.add(f, *accept_args, **accept_kwargs)
        return f
    return wrap

