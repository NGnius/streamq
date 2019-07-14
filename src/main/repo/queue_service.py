'''
Queue retrieval and saving to the database

Created 2019-06-04 by NGnius
'''
from ..repo import gherkin
from ..repo import sound_service
from ..objects import queue

gherkin.add_table('queues', 'id INTEGER PRIMARY KEY, bytes BLOB')

def get_queue(id, create=True):
    # TODO: handle upgrades from old gherkined objects
    if id >= 0:
        q = gherkin.load_object(table='queues', id=id)
    else:
        # DO NOT USE NEGATIVE IDs IN PRODUCTION!
        # TODO: warn/error if testing mode not detected
        q = None
    if q is None and create is True:
        q = queue.SoundQueue(id=id)
    return q

def save_queue(q):
    if q.id is None:
        q.id = gherkin.max_in_column(table='queues', column='id', default=-1)+1
    row = gherkin.fetch_one('SELECT id FROM queues WHERE id=?', (q.id,))
    if row is None:
        gherkin.execute('INSERT INTO queues (id) VALUES (?)', (q.id,))
    gherkin.save_object(q, table='queues')

def update_sounds(q):
    sounds = dict()  # cache of sounds
    # update sounds
    for i in range(len(q.sounds)):
        if q.sounds[i].id is not None:
            s_id = q.sounds[i].id
            if s_id not in sounds:
                new_sound = sound_service.get_sound(s_id)
                if new_sound is not None:
                    sounds[s_id] = new_sound
                    q.sounds[i] = new_sound
            else:
                q.sounds[i] = sounds[s_id]
        else:
            # NOTE: Sound with no id in SoundQueue is considered a design error!
            pass
    # update effective_queue
    for i in range(len(q.effective_queue)):
        if q.effective_queue[i].id is not None:
            s_id = q.effective_queue[i].id
            if s_id not in sounds:
                new_sound = sound_service.get_sound(s_id)
                if new_sound is not None:
                    sounds[s_id] = new_sound
                    q.effective_queue[i] = new_sound
            else:
                q.effective_queue[i] = sounds[s_id]
        else:
            # NOTE: Sound with no id in SoundQueue is considered a design error!
            pass
    return q

def save_sounds(q):
    for s in q.sounds:
        sound_service.save_sound(s)
    for s in q.effective_queue:
        sound_service.save_sound(s)
