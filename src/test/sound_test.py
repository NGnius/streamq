import unittest
from ..main.objects import sound

class SoundTest(unittest.TestCase):
    def test_no_id(self):
        s = sound.Sound(id=None)

        self.assertEqual(s.metadata, dict())
        self.assertEqual(s.id, None)

    def test_id(self):
        s = sound.Sound(id=-1)

        self.assertEqual(s.metadata, dict())
        self.assertEqual(s.id, -1)
