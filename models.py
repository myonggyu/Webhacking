from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

# ── 사용자 ─────────────────────────────────────────

def get_user_by_username(username):
    return get_db().execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()

def get_user_by_id(user_id):
    return get_db().execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()

def create_user(username, password):
    db = get_db()
    db.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()

def verify_password(user, password):
    return check_password_hash(user['password'], password)

# ── 게시글 ─────────────────────────────────────────

def get_all_posts():
    return get_db().execute('''
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.author_id = users.id
        ORDER BY posts.id DESC
    ''').fetchall()

def get_post(post_id):
    return get_db().execute('''
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.author_id = users.id
        WHERE posts.id = ?
    ''', (post_id,)).fetchone()

def create_post(title, content, author_id):
    db = get_db()
    db.execute(
        'INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)',
        (title, content, author_id)
    )
    db.commit()

def delete_post(post_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()

# ── 관리자 ─────────────────────────────────────────

def get_all_users():
    return get_db().execute(
        'SELECT id, username, is_admin FROM users'
    ).fetchall()

def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE author_id = ?', (user_id,))
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()