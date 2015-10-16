import collections
import unittest

from six import with_metaclass ## python 2/3 compabitible metaclass

from mnd.dispatch import Dispatcher
from mnd.handler import Handler, handle

# we will test arg matching against instances of this Msg type
Msg = collections.namedtuple("Msg", "note type")

d = Dispatcher()


class MsgHandler(with_metaclass(Handler)):
    __metaclass__ = Handler

    def __init__(self):
        self.was_called = False

    @handle(d)
    def default(self):
        self.was_called = True


class DispatchMethodsTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_handled(self):
        global d
        mh = MsgHandler()
        d.dispatch()
        self.assertTrue(mh.was_called)

