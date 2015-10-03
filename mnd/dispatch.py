"""
>>> d = Dispatcher()
>>> @handler(d, blah=1)
>>> def blah(blah=None):
...     print "got blah: ", blah
>>> d.dispatch(blah(blah=2))
>>> d.dispatch(blah(blah=1))
got blah: 1
"""

from match import args_match
import json

class Dispatcher(object):    
    """
    Dispatches matching events.
    """
    # TODO - make a version with more intelligent matching
    #        or args to handlers.
    def __init__(self):
        self.handlers = {}  # handler: rules
    
    def add(self, handler, *accept_args, **accept_kwargs):
        """
        Add a new handler 
        """
        
        # Dict is not hashable, so use hacky solution of converting to json :(
        key = json.dumps(dict(args=accept_args, kwargs=accept_kwargs))
        self.handlers[key] = (handler, accept_args, accept_kwargs)
    
    def dispatch(self, *args, **kwargs):
        # Test against all valid arguments...
        for handler, accept_args, accept_kwargs in self.handlers.values():
            if args_match(accept_args, accept_kwargs, *args, **kwargs):
                handler(*args, **kwargs)


def handle(dispatcher, *accept_args, **accept_kwargs):
    """
    :dispatcher: dispatcher to recieve events from
    :accept_args:   args to match on
    :accept_kwargs: kwargs to match on
    """
    def wrap(f):
        dispatcher.add(f, *accept_args, **accept_kwargs)
        return dispatcher.dispatch
    return wrap
