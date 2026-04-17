from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from models import get_all_posts, get_post, create_post, delete_post
from datetime import date

board = Blueprint('board', __name__)

def login_required():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.')
        return redirect(url_for('auth.login'))
    return None

@board.route('/')
def index():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response
    posts = get_all_posts()
    # 오늘 날짜를 템플릿에 넘겨 '오늘의 글' 카운트에 활용
    return render_template('board.html', posts=posts, now_date=str(date.today()))

@board.route('/write', methods=['GET', 'POST'])
def write():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        title   = request.form['title'].strip()
        content = request.form['content'].strip()

        if not title or not content:
            flash('제목과 내용을 모두 입력해주세요.')
        else:
            create_post(title, content, session['user_id'])
            return redirect(url_for('board.index'))

    return render_template('write.html')

@board.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    post = get_post(post_id)
    if post is None:
        abort(404)

    # 작성자 본인 또는 관리자만 삭제 가능
    if post['author_id'] != session['user_id'] and not session.get('is_admin'):
        abort(403)

    delete_post(post_id)
    return redirect(url_for('board.index'))