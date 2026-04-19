# 게시글 목록, 상세보기, 작성, 삭제 기능을 담당하는 게시판 라우트 파일입니다.
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models import (
    get_all_posts,
    get_post_by_id,
    create_post,
    delete_post,
    get_total_posts_count,
    get_today_posts_count
)

board_bp = Blueprint("board", __name__)


@board_bp.route("/")
def index():
    # 홈 화면에서 통계와 최신 게시글 목록을 보여줍니다.
    posts = get_all_posts()
    total_posts = get_total_posts_count()
    today_posts = get_today_posts_count()

    return render_template(
        "index.html",
        posts=posts,
        total_posts=total_posts,
        today_posts=today_posts
    )


@board_bp.route("/board")
def board_list():
    # 게시판 전용 페이지에서 전체 게시글 목록을 보여줍니다.
    posts = get_all_posts()
    total_posts = get_total_posts_count()
    today_posts = get_today_posts_count()

    return render_template(
        "board.html",
        posts=posts,
        total_posts=total_posts,
        today_posts=today_posts
    )


@board_bp.route("/write", methods=["GET", "POST"])
def write():
    # 로그인한 사용자가 새 게시글을 작성할 수 있도록 처리합니다.
    if "user_id" not in session:
        flash("글 작성은 로그인 후 가능합니다.")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("제목과 내용을 모두 입력해주세요.")
            return redirect(url_for("board.write"))

        create_post(
            title=title,
            content=content,
            author=session["username"],
            user_id=session["user_id"]
        )

        flash("게시글이 작성되었습니다.")
        return redirect(url_for("board.index"))

    return render_template("write.html")


@board_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    # 선택한 게시글의 상세 내용을 보여줍니다.
    post = get_post_by_id(post_id)

    if post is None:
        abort(404)

    return render_template("post_detail.html", post=post)


@board_bp.route("/delete/<int:post_id>", methods=["POST"])
def remove_post(post_id):
    # 작성자 본인 또는 관리자가 게시글을 삭제할 수 있도록 처리합니다.
    if "user_id" not in session:
        flash("삭제 권한이 없습니다.")
        return redirect(url_for("auth.login"))

    post = get_post_by_id(post_id)
    if post is None:
        abort(404)

    is_admin = session.get("role") == "admin"
    is_author = session.get("username") == post["author"]

    if not is_admin and not is_author:
        flash("본인 글 또는 관리자만 삭제할 수 있습니다.")
        return redirect(url_for("board.post_detail", post_id=post_id))

    delete_post(post_id)
    flash("게시글이 삭제되었습니다.")
    return redirect(url_for("board.index"))