'''
Audio metadata using mutagen

Created 2019-06-02 by NGnius
'''
from ..repo import file_service
import mutagen
from io import BytesIO

POTENTIAL_METADATA_TAGS = ['album', 'artist', 'title', 'tracknumber', 'albumartist', 'date', 'genre']

def audio_metadata(file_id):
    audio_file = file_service.get_file(file_id, file_like=True)
    return audio(audio_file)

def audio(file):
    result = dict()
    try:
        _mutagen_file = mutagen.File(file, easy=True)
    except mutagen.MutagenError:
        return result
    if _mutagen_file is None:
        # file is likely not audio
        return result
    tags = _mutagen_file.tags
    for tag in POTENTIAL_METADATA_TAGS:
        try:
            result[tag] = tags[tag][0]
        except KeyError:
            pass
    result['format'] = type(_mutagen_file).__name__.lower().replace('easy', '') # TODO: make this less hacky
    return result
