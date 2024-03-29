'''
Created 2019-06-01 by NGnius
'''

from ..repo import gherkin
from .sound import Sound
from ..tools import codes
import random

CURRENT_VERSION = '0.0.0.1'

class SoundQueue():
    def __init__(self, id=None, sounds=list(), shuffle=False, repeat_all=False, repeat_one=False, index=-1):
        self.version = str(CURRENT_VERSION)
        self.id = id
        self.sounds = sounds
        self.effective_queue = self.sounds
        self.shuffle(mode=shuffle)
        self.repeat_all = repeat_all
        self.repeat_one = repeat_one
        self.index = index

    def __add__(self, obj):
        if isinstance(obj, Sound):
            if self._shuffle is True:
                self.effective_queue.append(obj)
            self.sounds.append(obj)
        elif isinstance(obj, SoundQueue):
            for s in obj.sounds:
                if self._shuffle is True:
                    self.effective_queue.append(s)
                self.sounds.append(s)
        else:
            raise TypeError("Only Sound and SoundQueue objects can be added to a SoundQueue")
        # adding to a shuffle queue without an index should add to random spot
        self.shuffle(mode=self._shuffle)
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
        return self.effective_queue[i]

    def add(self, obj, index=None):
        '''Like + operator, but index can be used to insert into a specific location'''
        if index is None:
            self += obj
        else:
            if isinstance(obj, Sound):
                if self._shuffle is True:
                    self.effective_queue.insert(index, obj)
                self.sounds.insert(index, obj)
            elif isinstance(obj, SoundQueue):
                for s in obj.sounds[::-1]:
                    if self._shuffle is True:
                        self.effective_queue.insert(index, s)
                    self.sounds.insert(index, s)
            else:
                raise TypeError("Only Sound and SoundQueue objects can be added to a SoundQueue")

    def shuffle(self, mode=True):
        self._shuffle = mode
        if self._shuffle is True:
            upcoming_sounds = self.effective_queue[self.index:]
            random.shuffle(upcoming_sounds)
            self.effective_queue = self.effective_queue[:self.index] + upcoming_sounds
        else:
            self.effective_queue = self.sounds

    def now(self):
        if (self.index < 0) or (self.index >= len(self.effective_queue)):
            return
        return self.effective_queue[self.index]

    def next(self):
        if self.repeat_one is True:
            return self.now()
        elif (self.index + 1) > len(self.effective_queue):
            if self.repeat_all is True:
                self.index = -1
            else:
                return
        elif (self.index + 1) == len(self.effective_queue) and self.repeat_all is True:
            self.index = -1
        self.index += 1
        return self.now()

    def previous(self):
        if (self.index - 1) < 0:
            if self.repeat_all is True:
                self.index = len(self.effective_queue)
            else:
                return
        self.index -= 1
        return self.now()

    def to_jsonable(self):
        items = list()
        for s in self.effective_queue:
            items.append(s.to_jsonable())
        return {
            'code': codes.id2code(self.id),
            'id': self.id,
            'index': self.index,
            'items': items,
            'repeat-all': self.repeat_all,
            'repeat-one': self.repeat_one,
            'shuffle': self._shuffle
            }

def upgrade(old_queue):
    # TODO: handle conversion from old gherkined objects
    pass
