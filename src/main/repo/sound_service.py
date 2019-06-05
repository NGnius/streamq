'''
Sound retrieval and saving to the database

Created 2019-06-04 by NGnius
'''
from ..repo import gherkin
from ..objects import sound

gherkin.add_table('sounds', 'id INTEGER PRIMARY KEY, bytes BLOB')

def get_sound(id):
    if id >= 0:
        s = gherkin.load_object(table='sounds', id=id)
    else:
        # DO NOT USE NEGATIVE IDs IN PRODUCTION!
        # TODO: warn/error if testing mode not detected
        s = None
    if s is None:
        s = sound.Sound(id=id)
    return s

def save_sound(s):
    row = gherkin.fetch_one('SELECT id FROM sounds WHERE id=?', (s.id,))
    if row is None:
        gherkin.execute('INSERT INTO sounds (id) VALUES (?)', (s.id,))
    gherkin.save_object(s, table='sounds')
