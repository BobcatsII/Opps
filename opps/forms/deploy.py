#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length
from opps.models import DeployLog, Version, Project, User


class CreateDeployForm(FlaskForm):
    hosts = [(1, '192.168.250.141'), (2, '172.18.1.152')]
    deploy_project = SelectField(label='项目名称', validators=[DataRequired()], choices=[] ,coerce=int)
    deploy_ip = SelectField(label='IP地址', validators=[DataRequired()], choices=hosts, coerce=int) 
    deploy_version = SelectField(label='选择版本', validators=[DataRequired()], choices=[], coerce=int)
    deploy_user = SelectField(label='选择用户', validators=[DataRequired()], choices=[], coerce=int)
    submit = SubmitField('确认部署')
    
    def __init__(self, *args, **kwargs):
        super(CreateDeployForm, self).__init__(*args, **kwargs)
        self.deploy_project.choices = [(deploy_name.id, deploy_name.project_name) for deploy_name in Project.query.order_by(Project.project_name).all()]
        self.deploy_version.choices = [(deploy_ver.id, deploy_ver.deploy_version) for deploy_ver in Version.query.order_by(Version.deploy_version).all()]
        self.deploy_user.choices = [(deploy_user.id, deploy_user.username) for deploy_user in User.query.order_by(User.username).all()]
