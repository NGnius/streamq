from ..objects.basecase import BaseCase
from ...main.objects import queue

class SoundQueueTest(BaseCase):
    def setUp(self):
        super().setUp()
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
        self.queue1.sounds = self.queue1.effective_queue = [sound1]
        self.queue2.sounds = self.queue2.effective_queue = [sound2]
        self.queue1 += self.queue2
        self.assertEqual(self.queue1.sounds, [sound1, sound2])
        self.assertEqual(self.queue2.sounds, [sound2])

        self.queue2.add(self.queue1, index=0)
        self.assertEqual(self.queue2.sounds, [sound1, sound2, sound2])

    def test_index(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = self.queue1.effective_queue = [sound1, sound2]

        self.assertEqual(self.queue1[0], sound1)
        self.assertEqual(self.queue1[1], sound2)

    def test_shuffle(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        sound3 = queue.Sound()
        self.queue1.sounds = self.queue1.effective_queue = [sound1, sound2, sound3]
        self.queue1.shuffle()

        self.assertTrue(self.queue1._shuffle)

    def test_next(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = self.queue1.effective_queue = [sound1, sound2]

        self.assertEqual(self.queue1.next(), sound1)
        self.assertEqual(self.queue1.next(), sound2)
        self.assertIsNone(self.queue1.next())
        self.assertEqual(self.queue1.index, len(self.queue1.effective_queue))

    def test_previous(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = self.queue1.effective_queue = [sound1, sound2]

        self.queue1.index = 2
        self.assertEqual(self.queue1.previous(), sound2)
        self.assertEqual(self.queue1.previous(), sound1)
        self.assertIsNone(self.queue1.previous())
        self.assertEqual(self.queue1.index, 0)

    def test_repeat1(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = self.queue1.effective_queue = [sound1, sound2]
        self.queue1.index = 1
        self.queue1.repeat_one = True

        self.assertEqual(self.queue1.next(), sound2)
        self.assertEqual(self.queue1.next(), sound2)
        self.assertEqual(self.queue1.index, 1)

    def test_repeatall(self):
        sound1 = queue.Sound()
        sound2 = queue.Sound()
        self.queue1.sounds = self.queue1.effective_queue = [sound1, sound2]
        self.queue1.index = 1
        self.queue1.repeat = True

        self.assertEqual(self.queue1.next(), sound1)
        self.assertEqual(self.queue1.index, 0)
        self.assertEqual(self.queue1.previous(), sound2)
        self.assertEqual(self.queue1.index, 1)
        self.assertEqual(self.queue1.next(), sound1)
        self.assertEqual(self.queue1.next(), sound2)
