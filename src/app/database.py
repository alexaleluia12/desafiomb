import sqlite3

from flask import g

import const

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(const.DATABASE_NAME)
        db.row_factory = sqlite3.Row
    return db

def close_connection_cl(app):
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
