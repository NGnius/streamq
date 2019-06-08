from ..objects.basecase import BaseCase
from ...main.repo import gherkin
from ...main.repo import file_service

class FileServiceTest(BaseCase):
    def setUp(self):
        super().setUp()
        with load_file('nonsound') as f:
            self.nonsound = f.read()
        with load_file('halfsound') as f:
            self.halfsound = f.read()

    def test_save(self):
        # new save
        file_service.save_file(0, self.halfsound)
        row = gherkin.fetch_one('SELECT id, bytes FROM files WHERE id=?', (0,))
        self.assertIsNotNone(row)
        self.assertEqual(row[1], self.halfsound)

        # overwrite save
        file_service.save_file(0, self.nonsound)
        row = gherkin.fetch_one('SELECT id, bytes FROM files WHERE id=?', (0,))
        self.assertIsNotNone(row)
        self.assertEqual(row[1], self.nonsound)

    def test_load(self):
        max_id = gherkin.max_in_column(table='files', column='id')
        halfsound_id = max_id + 11
        nonsound_id = max_id + 42
        gherkin.execute('INSERT INTO files (id, bytes) VALUES (?,?)', (halfsound_id,self.halfsound))
        gherkin.execute('INSERT INTO files (id, bytes) VALUES (?,?)', (nonsound_id,self.nonsound))

        self.assertEqual(file_service.get_file(halfsound_id), self.halfsound)
        self.assertEqual(file_service.get_file(nonsound_id, file_like=True).read(), self.nonsound)

    def test_safety(self):
        id = gherkin.max_in_column(table='files', column='id')+2
        file_service.save_file(id, self.halfsound)

        # loaded as filelike, save from .read()
        loaded_file = file_service.get_file(id, file_like=True)
        self.assertIsNotNone(loaded_file)
        file_bytes = loaded_file.read()
        self.assertEqual(file_bytes, self.halfsound)
        file_service.save_file(id, file_bytes)

        # loaded as bytes
        loaded_bytes = file_service.get_file(id)
        self.assertIsNotNone(loaded_bytes)
        self.assertEqual(loaded_bytes, self.halfsound)

def load_file(file):
    return open('./src/test/test_data/audio/'+file, 'rb')
