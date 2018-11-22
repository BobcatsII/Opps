#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length
from opps.models import DeployLog


class CreateDeployForm(FlaskForm):
    deploy_project = SelectField(label='项目名称', validators=[DataRequired()], choices=[] ,coerce=int)
    deploy_ip = SelectField(label='IP地址', validators=[DataRequired()], choices=[], coerce=int) 
    deploy_version = SelectField(label='选择版本', validators=[DataRequired()], choices=[], coerce=int)
    deploy_user = SelectField(label='选择用户', validators=[DataRequired()], choices=[], coerce=int)
    submit = SubmitField('确认部署')
    
    def __init__(self, *args, **kwargs):
        super(CreateDeployForm, self).__init__(*args, **kwargs)
        self.deploy_project.choices = [(deploy_item.id, deploy_item.dply_item) for deploy_item in DeployLog.query.order_by(DeployLog.dply_item).all()] 
        self.deploy_ip.choices = [(deploy_ip.id, deploy_ip.dply_ip) for deploy_ip in DeployLog.query.order_by(DeployLog.dply_ip).all()] 
        self.deploy_version.choices = [(deploy_ver.id, deploy_ver.dply_version) for deploy_ver in DeployLog.query.order_by(DeployLog.dply_version).all()] 
        self.deploy_user.choices = [(deploy_user.id, deploy_user.dply_user) for deploy_user in DeployLog.query.order_by(DeployLog.dply_user).all()] 

