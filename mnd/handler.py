"""
To make callbacks work with instance methods some things need to happen.

The handler decorator attaches instances of MNDInfo to functions to enable
the dispatcher to work with classes and instances via the Handler metaclass.

At instance creation time the metaclass converts finds any handlers with
MNDFunction, replaces them with MNDMethods + informs the dispatcher.
"""

import pickle
import weakref

from collections import defaultdict


class ArgSpec(object):
    def __init__(self, key=None, *accept_args, **accept_kwargs):
        if key is None:
            key = pickle.dumps(dict(args=accept_args, kwargs=accept_kwargs))

        self.key = key
        self.accept_args = accept_args
        self.accept_kwargs = accept_kwargs

    def __repr__(self):
        return "ArgSpec([A(%s), KW(%s)])" % (self.accept_args, self.accept_kwargs)

    @property
    def accepts(self):
        return self.accept_args, self.accept_kwargs


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
    def __init__(self, f, dispatcher, argspec):
        """
        :param f: callback function to call
        """
        self._wf = weakref.ref(f)
        self.bound_to = defaultdict(set)
        self.bind_to(argspec, dispatcher)
        MNDInfo.__init__(self, "function")

    def bind_to(self, argspec, dispatcher):
        """
        Add dispatcher for argspec
        """
        self.bound_to[argspec.key].add((argspec, dispatcher))
        dispatcher.add(self.f, argspec)

    @property
    def f(self):
        return self._wf()

    def unbind(self):
        """
        Unbind from dispatchers and target function.

        :return: set of tuples containing [argspec, dispatcher]
        """
        args_dispatchers = set()
        f = self._wf()
        if f is not None:
            for ad_list in self.bound_to.values():
                args_dispatchers.update(ad_list)
                for argspec, dispatcher in ad_list:
                    dispatcher.unbind(self.f, argspec)
            del f.__dict__['__mnd__']
        self.bound_to = {}
        return args_dispatchers


class MNDMethod(MNDInfo):
    def __init__(self, dispatcher, argspec):
        """
        :param m: callback method to call
        :param dispatcher: initial dispatcher
        """
        self.bound_to = defaultdict(set)
        MNDInfo.__init__(self, "method")

    def bind_to(self, instancemethod, argspec, dispatcher):
        """
        Add dispatcher for argspec
        """
        self.bound_to[argspec.key].add((argspec, dispatcher))
        dispatcher.add(instancemethod, argspec)


class MNDClass(MNDInfo):
    def __init__(self, bind_to):
        MNDInfo.__init__(self, "class")
        self.bind_to = bind_to


def bind_handler_methods(self, klassname):
    for name, ad_list in self.__mnd__.bind_to.items():
        m = getattr(self, name)
        for argspec, dispatcher in ad_list:
            mnd = m.__dict__.get('__mnd__')
            if mnd is None:
                mnd = MNDMethod(dispatcher, argspec)
                m.__dict__['__mnd__'] = mnd
                mnd.bind_to(m, argspec, dispatcher)


def base_mnds(bases):
    """
    :param bases: sequence of base classes
    :yield: mnd of any base classes
    """
    for base in bases:
        mnd = getattr(base, "__mnd__", None)
        if mnd is not None:
            yield mnd


class Handler(type):
    """
    Metaclass enables instance methods to be used as handlers.
    """
    def __new__(meta, name, bases, dct):
        bind_to = defaultdict(set)   # { method_name: ((argspec, dispatcher)...)}
        for mnd in base_mnds(bases):
            bind_to.update(mnd.bind_to)

        for mname, member in dct.items():
            mnd = getattr(member, "__mnd__", None)
            if mnd is not None and mnd.is_function:
                args_dispatchers = mnd.unbind()  # set
                bind_to[mname].update(args_dispatchers)  # ((argspec, dispatcher)...)

        dct['__mnd__'] = MNDClass(bind_to)

        # wrap __init__
        wrapped_init = dct.get('__init__')
        if wrapped_init is None:
            if bases:
                def wrapped_init(self, *args, **kwargs):
                    pass

        def __init__(self, *args, **kwargs):
            bind_handler_methods(self, name)
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

    Creates an MNDFunction instance which adds contains the
    argspec and adds the function to the dispatcher.
    """
    def wrap(f):
        argspec = ArgSpec(None, *accept_args, **accept_kwargs)
        mnd = MNDFunction(f, dispatcher, argspec)
        f.__mnd__ = mnd
        return f
    return wrap
