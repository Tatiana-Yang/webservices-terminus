from flask import g
import sqlite3

DATA_URL = "./database/db_terminus.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATA_URL)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_connection(request_string):
	cursor = get_db().cursor()
	cursor.execute(request_string)
	return cursor

def insert_into_db(request_string):
	cursor = get_db().cursor()
	cursor.execute(request_string)
	get_db().commit()