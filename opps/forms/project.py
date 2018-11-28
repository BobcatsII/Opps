#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  DecimalField
from wtforms.validators import DataRequired, Length
from opps.models import Project

class ProjectForm(FlaskForm):
    project_name = StringField('项目名称', validators=[DataRequired(), Length(1, 50)])
    project_type = StringField('项目类型', validators=[DataRequired(), Length(1, 50)])
    project_port = DecimalField('项目端口', validators=[DataRequired()])
    project_info = StringField('项目信息', validators=[DataRequired(), Length(1, 50)])
    project_stat = StringField('项目状态', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField('确认添加')
