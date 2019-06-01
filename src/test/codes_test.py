import unittest
from ..main.tools import codes

class CodesTest(unittest.TestCase):
    def test_2code(self):
        self.assertEqual(codes.id2code(0), 'A')
        self.assertEqual(codes.id2code(42), 'HB')

    def test_2id(self):
        self.assertEqual(0, codes.code2id('A'))
        self.assertEqual(42, codes.code2id('HB'))

    def test_safety(self):
        self.assertEqual(codes.code2id(codes.id2code(0)), 0)
        self.assertEqual(codes.id2code(codes.code2id('ABC')), 'ABC')
