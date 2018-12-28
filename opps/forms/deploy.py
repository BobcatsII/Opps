#-*- coding:utf-8 -*-

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField, SelectFieldBase, RadioField
from wtforms.validators import DataRequired, Length
from opps.models import DeployLog, Version, Project, User


class CreateDeployForm(FlaskForm):
    deploy_type = RadioField('项目种类', validators=[DataRequired()], choices=[('app','APP服务'),('conf','文件配置')], default='app')
    deploy_project = SelectField(label='项目名称', validators=[DataRequired()], choices=[])
    deploy_host = SelectField(label='主机地址', validators=[DataRequired()], choices=[]) 
    deploy_version = SelectField(label='选择版本', validators=[DataRequired()], choices=[])
    deploy_user = SelectField(label='选择用户', validators=[DataRequired()], choices=[])
    submit = SubmitField('确认部署')
    
    def __init__(self, *args, **kwargs):
        super(CreateDeployForm, self).__init__(*args, **kwargs)
        self.deploy_project.choices = [(deploy_name.project_name, deploy_name.project_name) for deploy_name in Project.query.filter_by(project_stat=1).order_by(Project.project_name).all()]
        self.deploy_version.choices = [(deploy_ver.deploy_version, deploy_ver.deploy_version) for deploy_ver in Version.query.order_by(Version.deploy_version).all()]
        self.deploy_user.choices = [(deploy_user.username, deploy_user.username) for deploy_user in User.query.order_by(User.username).all()]
        #self.deploy_host.choices = [(deploy_host.host_name, deploy_host.host_name) for deploy_host in Hosts.query.order_by(Hosts.host_name).all()]
        self.deploy_host.choices = [("192.168.227.129","192.168.227.129")]
