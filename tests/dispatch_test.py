import collections
import unittest

from mnd.dispatch import Dispatcher
from mnd.handler import handle

# we will test arg matching against instances of this Msg type
Msg = collections.namedtuple("Msg", "note type")

class DispatchTest(unittest.TestCase):
    cat_called = 0
    dog_called = 0
    librarian_called = 0

    def setUp(self):
        DispatchTest.cat_called = 0
        DispatchTest.dog_called = 0
        DispatchTest.librarian_called = 0
    
    def test_handle_match(self):
        talk = Dispatcher()
        @handle(talk, say="woof")
        def dog(say=None):
            DispatchTest.dog_called += 1

        @handle(talk, say="miaow")
        def cat(say=None):
            DispatchTest.cat_called += 1

        @handle(talk, say="sssh")
        def librarian(say=None):
            DispatchTest.librarian_called += 1

        def say(msg):
            talk.dispatch(say=msg)
        
        say("woof")
        self.assertEqual(DispatchTest.dog_called, 1)
        self.assertEqual(DispatchTest.cat_called, 0)

        say("miaow")
        self.assertEqual(DispatchTest.dog_called, 1)
        self.assertEqual(DispatchTest.cat_called, 1)

        self.assertEqual(DispatchTest.librarian_called, 0)

    #def test_attrs_match(self):
    #    msg

