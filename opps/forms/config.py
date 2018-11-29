#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField, SelectFieldBase
from wtforms.validators import DataRequired, Length
from opps.models import User, Config

class CreateConfigForm(FlaskForm):
    item_name = StringField('项目名', validators=[DataRequired(), Length(1, 20)])
    conf_version = StringField('版本', validators=[DataRequired(), Length(1, 20)])
    conf_file = StringField('配置文件名', validators=[DataRequired(), Length(1, 20)])
    conf_user = SelectField(label='选择用户', validators=[DataRequired()], choices=[]) 
    submit = SubmitField('确认')

    def __init__(self, *args, **kwargs):
        self.conf_user.choices = [(conf_user.username, conf_user.username) for conf_user in User.query.order_by(User.username).all()]
