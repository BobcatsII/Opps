#-*- coding:utf-8 -*-

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField, SelectFieldBase, TextAreaField
from wtforms.validators import DataRequired, Length
from opps.models import User, Config, Version, Project

class CreateConfigForm(FlaskForm):
    item_name = SelectField(label='项目名称', validators=[DataRequired()], choices=[])
    conf_version = SelectField(label='配置版本', validators=[DataRequired()], choices=[])
    conf_file = SelectField(label='配置文件', validators=[DataRequired()], choices=[])
    conf_user = SelectField(label='操作用户', validators=[DataRequired()], choices=[])  
    conf_text = TextAreaField('配置内容', validators=[DataRequired()])
    submit = SubmitField('保存配置')

    def __init__(self, *args, **kwargs):
        super(CreateConfigForm, self).__init__(*args, **kwargs)
        self.conf_user.choices = [(conf_user.username, conf_user.username) for conf_user in User.query.order_by(User.username).all()]
        self.conf_version.choices = [(conf_ver.config_version, conf_ver.config_version) for conf_ver in Version.query.order_by(Version.config_version).all()]
        #self.conf_file.choices = [('config.py','config.py'), ('start_sss.py', 'start_sss.py')]
        self.conf_file.choices =  sorted(current_app.config['MODULE'])
        self.item_name.choices = [(item_name.project_name, item_name.project_name) for item_name in Project.query.filter_by(project_stat=1).order_by(Project.project_name).all()]
