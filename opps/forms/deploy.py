#-*- coding:utf-8 -*-

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField, SelectFieldBase, RadioField
from wtforms.validators import DataRequired, Length
from opps.models import DeployLog, Version, Project, User


class CreateDeployForm(FlaskForm):
    deploy_type = RadioField('项目种类', validators=[DataRequired()], choices=[('app','APP服务'),('conf','CONF配置')], default='app')
    #app
    deploy_project_app = SelectField(label='项目名称', validators=[DataRequired()], choices=[])
    deploy_version_app = SelectField(label='选择版本', validators=[DataRequired()], choices=[])
    #conf
    deploy_project_conf = SelectField(label='项目名称', validators=[DataRequired()], choices=[])
    deploy_version_conf = SelectField(label='选择版本', validators=[DataRequired()], choices=[])
    #主机
    deploy_host = SelectField(label='主机地址', validators=[DataRequired()], choices=[]) 
    #用户
    deploy_user = SelectField(label='选择用户', validators=[DataRequired()], choices=[])
    submit = SubmitField('确认部署')
    
    def __init__(self, *args, **kwargs):
        super(CreateDeployForm, self).__init__(*args, **kwargs)
        #app
        self.deploy_project_app.choices = [(deploy_name_app.project_name, deploy_name_app.project_name) for deploy_name_app in Project.query.filter_by(project_stat=1,project_type='app').order_by(Project.project_name).all()]
        self.deploy_version_app.choices = [(deploy_ver_app.deploy_version, deploy_ver_app.deploy_version) for deploy_ver_app in Version.query.order_by(Version.deploy_version).all()]

        #conf
        self.deploy_project_conf.choices = [(deploy_name_conf.project_name, deploy_name_conf.project_name) for deploy_name_conf in Project.query.filter_by(project_stat=1,project_type='conf').order_by(Project.project_name).all()]
        self.deploy_version_conf.choices = [(deploy_ver_conf.config_version, deploy_ver_conf.config_version) for deploy_ver_conf in Version.query.order_by(Version.config_version).all()]

        #主机
        #self.deploy_host.choices = [(deploy_host.host_name, deploy_host.host_name) for deploy_host in Hosts.query.order_by(Hosts.host_name).all()]
        self.deploy_host.choices = [("192.168.227.129","192.168.227.129")]

        #用户
        self.deploy_user.choices = [(deploy_user.username, deploy_user.username) for deploy_user in User.query.order_by(User.username).all()]
