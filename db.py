import sqlite3
from flask import g

DATABASE = 'board.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            author_id  INTEGER NOT NULL,
            created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    ''')

    # 관리자 계정 생성 (중복 방지)
    existing = db.execute(
        'SELECT id FROM users WHERE username = ?', ('admin',)
    ).fetchone()

    if not existing:
        from werkzeug.security import generate_password_hash
        db.execute(
            'INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
            ('admin', generate_password_hash('admin1234'), 1)
        )

    db.commit()
    db.close()