'''
File retrieval and saving to the database

Created 2019-06-02 by NGnius
'''
from ..repo import gherkin
from io import BytesIO

gherkin.add_table('files', 'id INTEGER PRIMARY KEY, bytes BLOB')

def get_file(id, file_like=False):
    if id >= 0:
        row = gherkin.fetch_one('SELECT bytes FROM files WHERE id=?', (id,))
    else:
        # DO NOT USE NEGATIVE IDs IN PRODUCTION!
        # TODO: warn/error if testing mode not detected
        row = None
    if row is None:
        if file_like is True:
            return BytesIO(b'')
        else:
            return b''
    data = row[0]
    if file_like is True:
        return BytesIO(data)
    else:
        return data

def save_file(id, data):
    max_id = gherkin.max_in_column(table='sounds', column='id')
    if id > max_id:
        gherkin.execute('INSERT INTO files VALUES id (?)', (id,))
    gherkin.execute('UPDATE files SET file=? WHERE id=?', (data, id))
