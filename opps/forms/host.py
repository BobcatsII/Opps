#-*- coding:utf-8 -*-

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, DecimalField
from wtforms.validators import DataRequired, Length
from opps.models import Hosts


class HostForm(FlaskForm):
    host = StringField('主机地址', validators=[DataRequired(), Length(1, 20)])
    host_type = SelectField(label='所属类型', validators=[DataRequired()], choices=[])
    submit = SubmitField('确认添加')
    
    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        self.host_type.choices =  sorted(current_app.config['SYSTEM'])


