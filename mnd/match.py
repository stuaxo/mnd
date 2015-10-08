"""
Argument matching.
"""
from operator import eq, contains
from collections import namedtuple


class InvalidArg:
    def __bool__(self):
        return False


def arg_comparitor(name):
    """
    :param arg name
    :return: pair containing  name, comparitor

    given an argument name, munge it and return a proper comparitor

    >>> get_arg_cmp("a")
    a, operator.eq

    >>> get_arg_cmp("a__in")
    a, operator.contains
    """
    if name.endswith("__in"):
        return name[:-4], contains
    else:
        return name, eq

    
    
def arg_match(m_arg, arg, comparitor=eq, default=True):
    """
    :param m_arg: value to match against or callable
    :param arg: arg to match
    :param comparitor:  function that returns True if m_arg and arg match
    :param default: will be returned if m_arg is None
    

    if m_arg is a callable it will be called with arg
    
    >>> arg_match(1, 1)
    True
    
    >>> arg_match(1, 2)
    True
    
    You can match by sub args by passing in a dict
    
    >>> from collections import namedtuple
    >>> Msg = namedtuple("msg", ["note", "type"])
    >>> m = Msg(note=1, type="note_on")
    >>> arg_match(dict(note=1), m)
    True
    
    """
    if m_arg is None:
        return default
    if isinstance(m_arg, dict):
        for name, value in m_arg.items():
            name, _comparitor = arg_comparitor(name)
            subarg = getattr(arg, name, InvalidArg)
            if subarg is InvalidArg:
                return subarg
            matched = arg_match(subarg, value, _comparitor, default)
            if not matched or matched is InvalidArg:
                return False
        return True
    else:
        if hasattr(m_arg, "__call__"):
            return m_arg(arg)
        else:
            return comparitor(arg, m_arg)


def args_match(m_args, m_kwargs, *args, **kwargs):
    """
    :param m_args:   values to match args against
    :param m_kwargs: values to match kwargs against
    :param arg: args to match
    :param arg: kwargs to match
    """
    if len(m_args) > len(args):
        return False
    for m_arg, arg in zip(m_args, args):
        matches = arg_match(m_arg, arg, eq)
        if not matches or matches is InvalidArg:
            return False  # bail out

    if m_kwargs:
        for name, m_arg in m_kwargs.items():
            name, comparitor = arg_comparitor(name)
            arg = kwargs.get(name)
            if not arg_match(m_arg, arg, comparitor):
                return False  # bail out
    return True

