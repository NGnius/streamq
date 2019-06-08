from ..objects.basecase import BaseCase
from ...main.repo import gherkin
from ...main.repo import sound_service
from ...main.objects.sound import Sound

class SoundServiceTest(BaseCase):
    def setUp(self):
        super().setUp()
        self.sound_id = gherkin.max_in_column(table='sounds', column='id', default=42) + 2
        gherkin.execute('INSERT INTO sounds (id) VALUES (?)', (self.sound_id,),  commit=True)
        s = Sound(id=self.sound_id)
        gherkin.save_object(s, table='sounds')

    def test_save(self):
        # new save
        id1 = 0
        s1 = Sound(id=id1)
        sound_service.save_sound(s1)
        sound_row = gherkin.fetch_one('SELECT id FROM sounds WHERE id=?', (id1,))
        self.assertIsNotNone(sound_row)
        self.assertEqual(sound_row[0], id1)

        # overwrite
        id2 = self.sound_id
        s2 = Sound(id=id2)
        sound_service.save_sound(s2)
        sound_row = gherkin.fetch_one('SELECT id FROM sounds WHERE id=?', (id2,))
        self.assertIsNotNone(sound_row)
        self.assertEqual(sound_row[0], id2)

    def test_load(self):
        id = self.sound_id
        s = sound_service.get_sound(id)
        self.assertIsNotNone(s)
        self.assertEqual(s.id, id)

    def test_safety(self):
        id1 = 0
        s1 = Sound(id=id1)
        sound_service.save_sound(s1)
        sound_row = gherkin.fetch_one('SELECT id FROM sounds where id=?', (id1,))

        s2 = sound_service.get_sound(id1)
        self.assertEqual(s2, s1)
