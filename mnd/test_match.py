import collections
import unittest

from mnd import arg_match

Msg = collections.namedtuple("Msg", "note type")

class ArgMatchTest(unittest.TestCase):
    def test_arg(self):
        self.assertTrue(arg_match(1, 1))

    def test_args(self):
        self.assertTrue(arg_match([1], [1]))

    def test_subarg(self):
        note1 = Msg(note=1, type="note_on")
        self.assertTrue(arg_match(dict(note=1), note1))

