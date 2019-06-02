'''
Created 2019-06-01 by NGnius
'''
from ..repo import gherkin
from ..tools import codes
from ..tools import metadata as md

class Sound():
    def __init__(self, id=None, metadata=None):
        self.id = id
        if isinstance(metadata, dict):
            self.metadata = metadata
        elif self.id is not None:
            self.populate_metadata()
        else:
            self.metadata = {}

    def to_jsonable(self):
        return {'id': self.id, 'code': codes.id2code(self.id), 'metadata':self.metadata}

    def populate_metadata(self):
        self.metadata = md.audio_metadata(self.id)
