from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import get_user_by_username, create_user, verify_password

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = get_user_by_username(username)

        if user and verify_password(user, password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            return redirect(url_for('board.index'))

        flash('아이디 또는 비밀번호가 올바르지 않습니다.')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not username or not password:
            flash('아이디와 비밀번호를 모두 입력해주세요.')
        elif get_user_by_username(username):
            flash('이미 사용 중인 아이디입니다.')
        else:
            create_user(username, password)
            flash('회원가입이 완료됐습니다. 로그인해주세요.')
            return redirect(url_for('auth.login'))

    return render_template('register.html')