from ..objects.basecase import BaseCase
from ...main.repo import gherkin
from ...main.repo import queue_service
from ...main.repo import sound_service
from ...main.objects.queue import SoundQueue
from ...main.objects.sound import Sound

class QueueServiceTest(BaseCase):
    def setUp(self):
        self.q_id = gherkin.max_in_column(table='queues', column='id', default=42) + 2
        gherkin.execute('INSERT INTO queues (id) VALUES (?)', (self.q_id,),  commit=True)
        q = SoundQueue(id=self.q_id)
        gherkin.save_object(q, table='queues')

    def test_save(self):
        # new save
        id1 = 0
        q1 = SoundQueue(id=id1)
        queue_service.save_queue(q1)
        q_row = gherkin.fetch_one('SELECT id FROM queues WHERE id=?', (id1,))
        self.assertIsNotNone(q_row)
        self.assertEqual(q_row[0], id1)

        # overwrite
        id2 = self.q_id
        q2 = SoundQueue(id=id2)
        queue_service.save_queue(q2)
        q_row = gherkin.fetch_one('SELECT id FROM queues WHERE id=?', (id2,))
        self.assertIsNotNone(q_row)
        self.assertEqual(q_row[0], id2)

    def test_load(self):
        id = self.q_id
        q = queue_service.get_queue(id)
        self.assertIsNotNone(q)
        self.assertEqual(q.id, id)

    def test_safety(self):
        id1 = 1
        q1 = SoundQueue(id=id1)
        queue_service.save_queue(q1)
        sound_row = gherkin.fetch_one('SELECT id FROM queues where id=?', (id1,))

        q2 = queue_service.get_queue(id1)
        self.assertEqual(q2, q1)

    def test_soundupdate(self):
        s1 = Sound(id=101)
        s1_n = Sound(id=101)
        s1_n.metadata = {'title':'<creative title here>'}

        s2 = Sound(id=102)
        s2_n = Sound(id=102)
        s2_n.metadata = {'artist':'Yomama'}

        sound_service.save_sound(s1_n)
        sound_service.save_sound(s2_n)

        q1 = SoundQueue(id=self.q_id, sounds=[s1, s2])
        q1.effective_queue = [s2, s1]
        queue_service.update_sounds(q1)
        self.assertEqual(q1.sounds, [s1_n, s2_n])

        q1._shuffle = True  # effective_queue and sounds cannot be assumed equal
        queue_service.update_sounds(q1)
        self.assertEqual(q1.effective_queue, [s2_n, s1_n])


    def test_soundsave(self):
        s1 = Sound(id=101, metadata={'title':'s1'})
        s2 = Sound(id=102, metadata={'title':'s2'})
        s3 = Sound(id=103, metadata={'title':'s3'})
        q1 = SoundQueue(id=self.q_id, sounds=[s1, s2])
        q1.effective_queue = [s1, s2, s3]
        queue_service.save_sounds(q1)
        self.assertEqual(sound_service.get_sound(s1.id).to_jsonable(), s1.to_jsonable())
        self.assertEqual(sound_service.get_sound(s2.id).to_jsonable(), s2.to_jsonable())
        # print(sound_service.get_sound(s3.id).to_jsonable() == s3.to_jsonable())
        # ^^^ Not necessarily True until after q1._shuffle is True (and q1's sounds saved)

        q1._shuffle = True  # effective_queue and sounds cannot be assumed equal
        queue_service.save_sounds(q1)
        self.assertEqual(sound_service.get_sound(s3.id).to_jsonable(), s3.to_jsonable())

    def test_nocreate(self):
        id = 404
        q1 = queue_service.get_queue(id, create=False)

        self.assertIsNone(q1)
