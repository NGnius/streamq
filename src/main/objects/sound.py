'''
Created 2019-06-01 by NGnius
'''
from ..repo import gherkin
from ..tools import codes
from ..tools import metadata as md

class Sound():
    def __init__(self, id=None, metadata=None):
        self.version = 0
        self.id = id
        if isinstance(metadata, dict):
            self.metadata = metadata
        elif self.id is not None:
            self.populate_metadata()
        else:
            self.metadata = {}

    def __eq__(self, other):
        if not isinstance(other, Sound):
            return False
        elif self.id is None or other.id is None:
            return self.to_jsonable() == other.to_jsonable()
        else:
            return self.id == other.id

    def to_jsonable(self):
        return {
                'id': self.id,
                'code': codes.id2code(self.id) if self.id is not None else None,
                'metadata':self.metadata
                }

    def populate_metadata(self):
        self.metadata = md.audio_metadata(self.id)
