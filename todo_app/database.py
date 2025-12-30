
import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE', 'todo.db')
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    conn = get_db()
    conn.executescript("""
        DROP TABLE IF EXISTS tasks;
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT
        );
    """)
    conn.commit()

# Call init_db() once to set up the DB
if __name__ == '__main__':
    init_db()