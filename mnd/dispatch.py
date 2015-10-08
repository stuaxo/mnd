"""
Dispatcher
"""

from mnd.match import args_match

import pickle
import logging

mnd_logger = logging.getLogger('mnd')
mnd_logger.setLevel(logging.DEBUG)
ch=logging.StreamHandler()
mnd_logger.addHandler(ch)

class Dispatcher(object):    
    """
    Dispatches matching events.
    """
    # TODO - make a version with more intelligent matching
    #        or args to handlers.
    def __init__(self):
        """
        Dispatch matching events

        >>> d = Dispatcher()
        >>> @handler(d, msg="hello")
        >>> def say(msg=None):
        ...     print "got message: ", msg
        >>> d.dispatch(msg="gets filtered out...")
        >>> d.dispatch(msg="hello")
        got message: hello
        """
        self.handlers = {}  # handler: rules
    
    def add(self, handler, *accept_args, **accept_kwargs):
        """
        Add a new handler that will be called when args match accept_args
        or kwargs match accept_kwargs
        """
        
        # Dict is not hashable, so use hacky solution of converting to json :(
        key = pickle.dumps(dict(args=accept_args, kwargs=accept_kwargs))
        self.handlers[key] = (handler, accept_args, accept_kwargs)
    
    def dispatch(self, *args, **kwargs):
        """
        Call handlers that match args or kwargs

        :return: set of handlers called
        """
        called_handlers = set()
        for handler, accept_args, accept_kwargs in self.handlers.values():
            if handler in called_handlers:
                continue
            else:
                if args_match(accept_args, accept_kwargs, *args, **kwargs):
                    called_handlers.add(handler)
                    handler(*args, **kwargs)
        
        return called_handlers

class LoggingDispatcher(Dispatcher):
    def __init__(self, name, logger=None):
        global mnd_logger
        Dispatcher.__init__(self)
        self.name = name
        if logger is None:
            self.logger = mnd_logger
        else:
            self.logger = logger
    
    def dispatch(self, *args, **kwargs):
        self.logger.info("%s dispatch %r %r", self.name, args, kwargs)
        try:
            called_handlers = super(LoggingDispatcher, self).dispatch(*args, **kwargs)
            for handler in called_handlers or []:
                self.logger.info("  %s called: %s %s", self.name, handler.__name__, handler)
            if not called_handlers:
                self.logger.info("  %s no matching handlers were found.", self.name)
        except Exception as e:
            self.logger.info(e)

def handle(dispatcher, *accept_args, **accept_kwargs):
    """
    :param dispatcher: dispatcher to recieve events from
    :param accept_args:   args to match on
    :param accept_kwargs: kwargs to match on
    Decorator to attach functions to dispatcher
    """
    def wrap(f):
        dispatcher.add(f, *accept_args, **accept_kwargs)
        return f
    return wrap

