#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, DecimalField
from wtforms.validators import DataRequired, Length
from opps.models import Version, User


class VersionForm(FlaskForm):
    deploy_version = StringField('项目版本(无新增用"-"表示)', validators=[DataRequired(), Length(1, 20)])
    config_version = StringField('配置版本(无新增用"-"表示)', validators=[DataRequired(), Length(1, 20)])
    add_user = SelectField(label='选择用户', validators=[DataRequired()], choices=[])
    submit = SubmitField('确认添加')
    
    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.add_user.choices = [(add_user.username, add_user.username) for add_user in User.query.order_by(User.username).all()]
