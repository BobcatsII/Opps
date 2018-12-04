#-*- coding:utf-8 -*-
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  IntegerField, SelectField
from wtforms.validators import DataRequired, Length
from opps.models import Project

class ProjectForm(FlaskForm):
    project_name = StringField('项目名称', validators=[DataRequired(), Length(1, 50)])
    project_type = SelectField(label='项目类型', validators=[DataRequired()], choices=[])
    project_port = IntegerField('项目端口', validators=[DataRequired()])
    project_info = StringField('项目信息', validators=[DataRequired(), Length(1, 50)])
    submit = SubmitField('确认添加')
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.project_type.choices =  sorted(current_app.config['SYSTEM'])
