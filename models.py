# 게시글과 사용자 데이터를 조회/추가/삭제하는 DB 접근 함수들을 모아둔 파일입니다.
from db import get_db_connection


def get_all_posts():
    # 모든 게시글을 최신순으로 조회합니다.
    conn = get_db_connection()
    posts = conn.execute("""
        SELECT id, title, content, author, user_id, created_at
        FROM posts
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return posts


def get_post_by_id(post_id):
    # 게시글 ID로 상세 게시글 1건을 조회합니다.
    conn = get_db_connection()
    post = conn.execute("""
        SELECT id, title, content, author, user_id, created_at
        FROM posts
        WHERE id = ?
    """, (post_id,)).fetchone()
    conn.close()
    return post


def create_post(title, content, author, user_id):
    # 새 게시글을 저장합니다.
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO posts (title, content, author, user_id, created_at)
        VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
    """, (title, content, author, user_id))
    conn.commit()
    conn.close()


def delete_post(post_id):
    # 게시글 ID에 해당하는 게시글을 삭제합니다.
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()


def get_total_posts_count():
    # 전체 게시글 수를 반환합니다.
    conn = get_db_connection()
    row = conn.execute("SELECT COUNT(*) AS cnt FROM posts").fetchone()
    conn.close()
    return row["cnt"]


def get_today_posts_count():
    # 오늘 작성된 게시글 수를 반환합니다.
    conn = get_db_connection()
    row = conn.execute("""
        SELECT COUNT(*) AS cnt
        FROM posts
        WHERE date(created_at) = date('now', 'localtime')
    """).fetchone()
    conn.close()
    return row["cnt"]


def get_user_by_username(username):
    # 아이디로 사용자 1명을 조회합니다.
    conn = get_db_connection()
    user = conn.execute("""
        SELECT id, username, password, role, created_at
        FROM users
        WHERE username = ?
    """, (username,)).fetchone()
    conn.close()
    return user


def create_user(username, password_hash):
    # 일반 사용자 계정을 생성합니다.
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, 'user')
    """, (username, password_hash))
    conn.commit()
    conn.close()


def get_all_users():
    # 전체 사용자 목록을 최신순으로 조회합니다.
    conn = get_db_connection()
    users = conn.execute("""
        SELECT id, username, role, created_at
        FROM users
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return users