from ..objects.basecase import BaseCase
from ...main.objects import sound

class SoundTest(BaseCase):
    def test_no_id(self):
        s = sound.Sound(id=None)

        self.assertEqual(s.metadata, dict())
        self.assertEqual(s.id, None)

    def test_id(self):
        s = sound.Sound(id=42)

        self.assertEqual(s.metadata, dict())
        self.assertEqual(s.id, 42)

    def test_eq(self):
        s1 = sound.Sound(id=42)
        s2 = sound.Sound()

        self.assertNotEqual(s1, s2)

        s2.metadata = {'artist':'Pear'}
        self.assertNotEqual(s1, s2)

        s3 = sound.Sound(id=42)
        self.assertEqual(s1, s3)

        s3.metadata = {'title':'Watermelon'}
        self.assertEqual(s1, s3)

        s4 = sound.Sound()
        self.assertNotEqual(s2, s4)

        s4.metadata = {'artist':'Pear'}
        self.assertEqual(s2, s4)
