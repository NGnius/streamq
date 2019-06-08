from ..objects.basecase import BaseCase
from ...main.tools import metadata

class MetadataTest(BaseCase):
    def test_nonsound(self):
        file = load_file('nonsound')
        data = metadata.audio(file)
        # metadata should be empty since it's not even audio
        self.assertEqual(data, dict())
        file.close()

    def test_halfsound(self):
        file = load_file('halfsound')
        # NOTE: halfsound is actually an audio file. "Half" refers to missing tags
        data = metadata.audio(file)
        self.assertNotEqual(data, dict())
        self.assertEqual(data['artist'], 'Monzy')
        self.assertEqual(data['title'], 'Kill Dash Nine')
        self.assertEqual(data['date'], '2006')
        self.assertEqual(data['genre'], 'Rap')
        self.assertEqual(data['format'], 'mp3')
        file.close()

def load_file(file):
    return open('./src/test/test_data/audio/'+file, 'rb')
