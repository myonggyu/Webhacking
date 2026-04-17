from flask import Blueprint, render_template, redirect, url_for, session, flash, abort
from models import get_all_users, get_all_posts, delete_user, delete_post

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required():
    if not session.get('is_admin'):
        abort(403)

@admin_bp.route('/')
def dashboard():
    admin_required()
    users = get_all_users()
    posts = get_all_posts()
    return render_template('admin.html', users=users, posts=posts)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def remove_user(user_id):
    admin_required()
    if user_id == session['user_id']:
        flash('자기 자신은 삭제할 수 없습니다.')
        return redirect(url_for('admin.dashboard'))
    delete_user(user_id)
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def remove_post(post_id):
    admin_required()
    delete_post(post_id)
    return redirect(url_for('admin.dashboard'))