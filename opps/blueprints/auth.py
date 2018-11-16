#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from opps.emails import send_confirm_email, send_reset_password_email
from opps.extensions import db
from opps.forms.auth import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from opps.models import User
from opps.settings import Operations
from opps.emails import send_confirm_email, send_reset_password_email
from opps.utils import generate_token, validate_token, redirect_back

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('登录成功.', 'info')
                return redirect_back()
            else:
                flash('你的账户已被屏蔽.', 'warning')
                return redirect(url_for('main.index'))
        flash('无效的邮箱或密码.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功.', 'info')
    return redirect(url_for('main.index'))
 

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('确认已发送的电子邮件，请检查你的收件箱.', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    if login_fresh():
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('auth/login.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('帐户已确认.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('令牌无效或过期.', 'danger')
        return redirect(url_for('.resend_confirm_email'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash('新的电子邮件已发送，请检查您的收件箱.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('密码重置电子邮件已发送，请检查您的收件箱.', 'info')
            return redirect(url_for('.login'))
        flash('无效的邮箱.', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            return redirect(url_for('main.index'))
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD,
                          new_password=form.password.data):
            flash('密码已更新.', 'success')
            return redirect(url_for('.login'))
        else:
            flash('链接无效或过期.', 'danger')
            return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)
