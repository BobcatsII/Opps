#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, DecimalField
from wtforms.validators import DataRequired, Length
from opps.models import Version


class VersionForm(FlaskForm):
    deploy_version = StringField('项目版本(无新增用"-"表示)', validators=[DataRequired(), Length(1, 20)])
    config_version = StringField('配置版本(无新增用"-"表示)', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('确认添加') 
