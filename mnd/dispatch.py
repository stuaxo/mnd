"""
Dispatcher
"""

from mnd.match import args_match
from mnd.handler import MNDFunction, handle

import collections
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
    # TODO - optimise data structures to speed this up
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
        self.handlers = collections.defaultdict(list)  # handler: rules
    
    def add(self, handler, argspec):
        self.handlers[argspec.key].append((handler, argspec))

    def unbind(self, handler, argspec):
        """
        handler will no longer be called if args match argspec

        :param argspec: instance of ArgSpec - args to be matched
        """
        self.handlers[argspec.key].remove((handler, argspec))
        if not len(self.handlers[argspec.key]):
            del self.handlers[argspec.key]
    
    def dispatch(self, *args, **kwargs):
        """
        Call handlers that match args or kwargs

        :return: set of handlers called
        """
        called_handlers = set()
        for handler_list in self.handlers.values():
            for handler, argspec in handler_list:
                accept_args, accept_kwargs = argspec.accepts
                if handler in called_handlers:
                    continue
                else:
                    if args_match(accept_args, accept_kwargs, *args, **kwargs):
                        called_handlers.add(handler)
                        handler(*args, **kwargs)
        
        return called_handlers