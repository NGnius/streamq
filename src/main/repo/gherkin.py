'''
Python pickle and SQLite3 wrapper.
This is not SQL secure.

Created by NGnius 2019-04-04
'''

import pickle
import sqlite3
import threading

database_path = None  # sqlite3 connection object (set by main.py)
database_connections = dict()
locks = dict()

def set_db(db):
    global database_path
    database_path = db

def save():
    database = get_connection()
    database.commit()

def get_connection():
    global database_connections, database_path
    thread_id = threading.get_ident()
    if thread_id not in database_connections:
        database_connections[thread_id] = sqlite3.connect(database_path)
    return database_connections[thread_id]

def fetch_all(sql, params=None):
    cursor = execute(sql, params=params)
    return cursor.fetchall()

def fetch_one(sql, params=None):
    cursor = execute(sql, params=params)
    return cursor.fetchone()

def execute(sql, params=None):
    database = get_connection()
    cursor = database.cursor()
    if params is not None:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    return cursor

def load_object(table='pickles', column='bytes', match='1=1', lock=False, no_fail=True):
    if lock:
        lock_row(table=table, match=match)
    row = fetch_one('SELECT %s FROM %s WHERE %s' % (column, table, match))
    if row is None:
        return
    bytes = row[0]
    return load_byte(bytes, no_fail=no_fail)

def save_object(object, table='pickles', column='bytes', match='1=0', release=False):
    database = get_connection()
    bytes = dump_byte(object)
    database.cursor().execute('UPDATE %s SET %s = ? WHERE %s' % (table, column, match), (bytes,))
    save()
    if release:
        unlock_row(table=table, match=match)

def add_columns(table, columns, commit=True):
    database = get_connection()
    cursor = database.cursor()
    cursor.execute('PRAGMA table_info(%s)' % table)
    column_names = [c[1] for c in cursor.fetchall()]
    for name in columns:
        if name not in column_names:
            cursor.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table, name, columns[name]) )
    if commit == True:
        save()

def add_table(table, columns):
    database = get_connection()
    cursor = database.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS %s (%s)' % (table, columns))

def load_byte(bytes, no_fail=True):
    try:
        return pickle.loads(bytes)
    except:
        if no_fail == True:
            return
        raise

def dump_byte(obj, no_fail=False):
    try:
        return pickle.dumps(obj)
    except:
        if no_fail == True:
            return
        raise

def lock_row(table='pickles', match='0=0', aquire=True):
    global locks
    row = fetch_one('SELECT id FROM %s WHERE %s' % (table, match))
    if row is None:
        return
    if table+str(row[0]) not in locks:
        locks[table+str(row[0])]= threading.Event()
        locks[table+str(row[0])].set()
    if aquire:
        while(not locks[table+str(row[0])].is_set()):
            locks[table+str(row[0])].wait()
    locks[table+str(row[0])].clear()

def unlock_row(table='pickles', match='1=0'):
    global locks
    row = fetch_one('SELECT id FROM %s WHERE %s' % (table, match))
    if row is None:
        return
    if table+str(row[0]) not in locks:
        locks[table+str(row[0])]= threading.Event()
    locks[table+str(row[0])].set()
