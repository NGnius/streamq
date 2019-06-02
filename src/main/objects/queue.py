'''
Created 2019-06-01 by NGnius
'''

from ..repo import gherkin
from .sound import Sound
from ..tools import codes

class SoundQueue():
    def __init__(self, id=None, sounds=list()):
        self.id = id
        self.sounds = sounds

    def __add__(self, obj):
        if isinstance(obj, Sound):
            self.sounds.append(obj)
        elif isinstance(obj, SoundQueue):
            for s in obj.sounds:
                self.sounds.append(s)
        else:
            raise TypeError("Only Sound and SoundQueue objects can be added to a SoundQueue")
        return self

    def __eq__(self, other):
        if not isinstance(other, SoundQueue):
            return self.sounds == other
        if self.id is None or other.id is None:
            return self.sounds == other.sounds
        else:
            return self.id == other.id

    def __len__(self):
        return len(self.sounds)

    def __str__(self):
        return str(self.sounds)

    def __getitem__(self, i):
        return self.sounds[i]

    def add(self, obj, index=None):
        '''Like + operator, but index can be used to insert into a specific location'''
        if index is None:
            self += obj
        else:
            if isinstance(obj, Sound):
                self.sounds.insert(index, obj)
            elif isinstance(obj, SoundQueue):
                for s in obj.sounds[::-1]:
                    self.sounds.insert(index, s)
            else:
                raise TypeError("Only Sound and SoundQueue objects can be added to a SoundQueue")

    def to_jsonable(self):
        items = list()
        for s in self.sounds:
            items.append(s.to_jsonable())
        return {'id': self.id, 'code': codes.id2code(self.id), 'items':items}
