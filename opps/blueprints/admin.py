# -*- coding: utf-8 -*-

from flask import render_template, flash, Blueprint, request, current_app
from flask_login import login_required
from opps.decorators import admin_required, permission_required
from opps.extensions import db
from opps.forms.admin import EditProfileAdminForm
from opps.models import Role, User
from opps.utils import redirect_back

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
@permission_required('MODERATE')
def index():
    user_count = User.query.count()
    locked_user_count = User.query.filter_by(locked=True).count()
    blocked_user_count = User.query.filter_by(active=False).count()
    return render_template('admin/index.html', user_count=user_count, locked_user_count=locked_user_count,
                           blocked_user_count=blocked_user_count)

@admin_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        role = Role.query.get(form.role.data)
        if role.name == 'Locked':
            user.lock()
        user.role = role
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.email = form.email.data
        user.active = form.active.data
        db.session.commit()
        flash('资料已更新.', 'success')
        return redirect_back()
    form.role.data = user.role_id
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.email.data = user.email
    form.active.data = user.active
    return render_template('admin/edit_profile.html', form=form, user=user)


@admin_bp.route('/block/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.block()
    flash('帐户已被屏蔽.', 'info')
    return redirect_back()


@admin_bp.route('/unblock/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def unblock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unblock()
    flash('屏蔽解除.', 'info')
    return redirect_back()


@admin_bp.route('/lock/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def lock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.lock()
    flash('账户被锁定.', 'info')
    return redirect_back()


@admin_bp.route('/unlock/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def unlock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unlock()
    flash('锁定解除.', 'info')
    return redirect_back()

@admin_bp.route('/manage/user')
@login_required
@permission_required('MODERATE')
def manage_user():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'locked', 'blocked', 'administrator', 'moderator'
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['OPPS_MANAGE_USER_PER_PAGE']
    administrator = Role.query.filter_by(name='Administrator').first()
    moderator = Role.query.filter_by(name='Moderator').first()

    if filter_rule == 'locked':
        filtered_users = User.query.filter_by(locked=True)
    elif filter_rule == 'blocked':
        filtered_users = User.query.filter_by(active=False)
    elif filter_rule == 'administrator':
        filtered_users = User.query.filter_by(role=administrator)
    elif filter_rule == 'moderator':
        filtered_users = User.query.filter_by(role=moderator)
    else:
        filtered_users = User.query

    pagination = filtered_users.order_by(User.member_since.desc()).paginate(page, per_page)
    users = pagination.items
    return render_template('admin/manage_user.html', pagination=pagination, users=users)


