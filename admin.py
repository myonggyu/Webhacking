# 관리자만 접근 가능한 사용자/게시글 현황 페이지를 담당하는 파일입니다.
from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import get_all_users, get_all_posts, get_total_posts_count, get_today_posts_count

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
def admin_home():
    # 관리자 페이지에서 전체 사용자와 게시글 현황을 보여줍니다.
    if session.get("role") != "admin":
        flash("관리자만 접근할 수 있습니다.")
        return redirect(url_for("board.index"))

    users = get_all_users()
    posts = get_all_posts()
    total_posts = get_total_posts_count()
    today_posts = get_today_posts_count()

    return render_template(
        "admin.html",
        users=users,
        posts=posts,
        total_posts=total_posts,
        today_posts=today_posts
    )