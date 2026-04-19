# 로그인, 회원가입, 로그아웃 기능을 담당하는 인증 라우트 파일입니다.
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_user_by_username, create_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # 사용자의 로그인 요청을 처리하고 세션을 생성합니다.
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("아이디와 비밀번호를 모두 입력해주세요.")
            return redirect(url_for("auth.login"))

        user = get_user_by_username(username)

        if user is None or not check_password_hash(user["password"], password):
            flash("아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect(url_for("auth.login"))

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        flash("로그인되었습니다.")
        return redirect(url_for("board.index"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # 새 사용자 회원가입을 처리합니다.
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        password_confirm = request.form.get("password_confirm", "").strip()

        if not username or not password or not password_confirm:
            flash("모든 항목을 입력해주세요.")
            return redirect(url_for("auth.register"))

        if password != password_confirm:
            flash("비밀번호 확인이 일치하지 않습니다.")
            return redirect(url_for("auth.register"))

        existing_user = get_user_by_username(username)
        if existing_user is not None:
            flash("이미 존재하는 아이디입니다.")
            return redirect(url_for("auth.register"))

        password_hash = generate_password_hash(password)
        create_user(username, password_hash)

        flash("회원가입이 완료되었습니다. 로그인해주세요.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    # 현재 로그인 세션을 종료합니다.
    session.clear()
    flash("로그아웃되었습니다.")
    return redirect(url_for("board.index"))