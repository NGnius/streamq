import unittest
from ..main.objects import queue

class SoundQueueTest(unittest.TestCase):
    def setUp(self):
        self.queue1 = queue.SoundQueue()
        self.queue2 = queue.SoundQueue()

    def test_sound_add(self):
        sound = queue.Sound()
        self.queue1 += sound
        self.assertEqual(sound, self.queue1.sounds[-1])

        self.queue2.add(sound, index=0)
        self.assertEqual(sound, self.queue2.sounds[0])

    def test_queue_add(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = [sound1]
        self.queue2.sounds = [sound2]
        self.queue1 += self.queue2
        self.assertEqual(self.queue1.sounds, [sound1, sound2])
        self.assertEqual(self.queue2.sounds, [sound2])

        self.queue2.add(self.queue1, index=0)
        self.assertEqual(self.queue2.sounds, [sound1, sound2, sound2])

    def test_index(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = [sound1, sound2]

        self.assertEqual(self.queue1[0], sound1)
        self.assertEqual(self.queue1[1], sound2)
