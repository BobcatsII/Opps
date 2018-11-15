# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, current_app, request, Blueprint
from flask_login import login_required, current_user, fresh_login_required, logout_user

from opps.decorators import confirm_required, permission_required
from opps.emails import send_confirm_email
from opps.extensions import db, avatars
from opps.forms.user import EditProfileForm, UploadAvatarForm, CropAvatarForm, ChangeEmailForm, ChangePasswordForm, DeleteAccountForm
from opps.models import User
from opps.settings import Operations
from opps.utils import generate_token, validate_token, redirect_back, flash_errors

user_bp = Blueprint('user', __name__)

@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user and user.locked:
        flash('你的帐户已被锁定.', 'danger')

    if user == current_user and not user.active:
        logout_user()

    return render_template('user/index.html', user=user)

@user_bp.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('资料已更新.', 'success')
        return redirect(url_for('.index', username=current_user.username))
    form.username.data = current_user.username
    return render_template('user/settings/edit_profile.html', form=form)

@user_bp.route('/settings/avatar')
@login_required
@confirm_required
def change_avatar():
    upload_form = UploadAvatarForm()
    crop_form = CropAvatarForm()
    return render_template('user/settings/change_avatar.html', upload_form=upload_form, crop_form=crop_form)

@user_bp.route('/settings/avatar/upload', methods=['POST'])
@login_required
@confirm_required
def upload_avatar():
    form = UploadAvatarForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = avatars.save_avatar(image)
        current_user.avatar_raw = filename
        db.session.commit()
        flash('图片已上传，请裁剪.', 'success')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))

@user_bp.route('/settings/avatar/crop', methods=['POST'])
@login_required
@confirm_required
def crop_avatar():
    form = CropAvatarForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        filenames = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
        current_user.avatar_s = filenames[0]
        current_user.avatar_m = filenames[1]
        current_user.avatar_l = filenames[2]
        db.session.commit()
        flash('头像已更新.', 'success')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))

@user_bp.route('/settings/change-password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit() and current_user.validate_password(form.old_password.data):
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('密码已更新.', 'success')
        return redirect(url_for('.index', username=current_user.username))
    return render_template('user/settings/change_password.html', form=form)


@user_bp.route('/settings/change-email', methods=['GET', 'POST'])
@fresh_login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        token = generate_token(user=current_user, operation=Operations.CHANGE_EMAIL, new_email=form.email.data.lower())
        send_confirm_email(to=form.email.data, user=current_user, token=token)
        flash('确认已发送的电子邮件，检查您的收件箱.', 'info')
        return redirect(url_for('.index', username=current_user.username))
    return render_template('user/settings/change_email.html', form=form)


@user_bp.route('/change-email/<token>')
@login_required
def change_email(token):
    if validate_token(user=current_user, token=token, operation=Operations.CHANGE_EMAIL):
        flash('邮箱已更新.', 'success')
        return redirect(url_for('.index', username=current_user.username))
    else:
        flash('令牌无效或过期.', 'warning')
        return redirect(url_for('.change_email_request'))

@user_bp.route('/settings/account/delete', methods=['GET', 'POST'])
@fresh_login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        db.session.delete(current_user._get_current_object())
        db.session.commit()
        flash('你自由了，再见!', 'success')
        return redirect(url_for('main.index'))
    return render_template('user/settings/delete_account.html', form=form)
