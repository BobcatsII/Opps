#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from opps.models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住账户')
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20),
                            Regexp('^[a-zA-Z0-9]*$',
                            message='用户名应仅包含 a-z, A-Z and 0-9.')])
    password = PasswordField('输入密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被使用.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用.')

class ForgetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()

class ResetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('输入密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField()
