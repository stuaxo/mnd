"""
>>> d = Dispatcher()
>>> @handler(d, msg="hello")
>>> def say(msg=None):
...     print "got message: ", msg
>>> d.dispatch(msg="gets filtered out..."))
>>> d.dispatch(msg="hello"))
got message: hello
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
        Add a new handler that will be called when args match accept_args
        or kwargs match accept_kwargs
        """
        
        # Dict is not hashable, so use hacky solution of converting to json :(
        key = json.dumps(dict(args=accept_args, kwargs=accept_kwargs))
        self.handlers[key] = (handler, accept_args, accept_kwargs)
    
    def dispatch(self, *args, **kwargs):
        """
        Call handlers that match args or kwargs
        """
        called_handlers = set()
        for handler, accept_args, accept_kwargs in self.handlers.values():
            if handler in called_handlers:
                continue
            else:
                called_handlers.add(handler)
            if args_match(accept_args, accept_kwargs, *args, **kwargs):
                handler(*args, **kwargs)


def handle(dispatcher, *accept_args, **accept_kwargs):
    """
    :dispatcher: dispatcher to recieve events from
    :accept_args:   args to match on
    :accept_kwargs: kwargs to match on

    Decorator to attach functions to dispatcher
    """
    def wrap(f):
        dispatcher.add(f, *accept_args, **accept_kwargs)
        return dispatcher.dispatch
    return wrap
