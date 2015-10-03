from collections import namedtuple
import mido


"""
Purely doing argument matching.
"""

class InvalidArg:
    pass


def arg_match(m_arg, arg, default=True):
    """
    :param m_arg: value to match against or callable
    :param arg: arg to match
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
        for name, value in m_arg.iteritems():
            subarg = getattr(arg, name, InvalidArg)
            if subarg is InvalidArg:
                return subarg
            matched = arg_match(subarg, value, default)
            if not matched:
                return matched
        return True
    else:
        if hasattr(m_arg, "__call__"):
            return m_arg(arg)
        else:
            return m_arg == arg


def args_match(m_args, m_kwargs, *args, **kwargs):
    """
    :param m_args:   values to match args against
    :param m_kwargs: values to match kwargs against
    :param arg: args to match
    :param arg: kwargs to match
    """
    if len(m_args) > args:
        return False
    for m_arg, arg in zip(m_args, args):
        if not arg_match(m_arg, arg):
            return False  # bail out

    if m_kwargs:
        for name, m_arg in m_kwargs.items():
            arg = kwargs.get(name)
            if not arg_match(m_arg, arg):
                return False  # bail out
    return True

