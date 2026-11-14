import sqlite3
from flask import current_app, g

SCHEMA = '''
CREATE TABLE IF NOT EXISTS enquiries (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 email TEXT NOT NULL,
 organisation TEXT,
 enquiry_type TEXT NOT NULL,
 subject TEXT NOT NULL,
 message TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'New' CHECK(status IN ('New','In Progress','Responded','Closed')),
 created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
'''

def get_db():
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(current_app.config['DATABASE'])
        except sqlite3.OperationalError:
            current_app.config['DATABASE'] = '/tmp/velcoris.db'
            g.db = sqlite3.connect(current_app.config['DATABASE'])
            g.db.executescript(SCHEMA)
            g.db.commit()
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def close_db(_=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        try:
            db = sqlite3.connect(app.config['DATABASE'])
            db.executescript(SCHEMA)
            db.commit()
            db.close()
        except sqlite3.OperationalError:
            app.config['DATABASE'] = '/tmp/velcoris.db'
            db = sqlite3.connect(app.config['DATABASE'])
            db.executescript(SCHEMA)
            db.commit()
            db.close()
    app.teardown_appcontext(close_db)
