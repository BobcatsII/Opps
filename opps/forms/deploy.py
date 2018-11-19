#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length

class CreateDeployForm(FlaskForm):
    deploy_project = SelectField('项目名称', coerce=int, default=1)
    deploy_ip = SelectField('目标IP', coerce=int, default=1)
    deploy_version = SelectField('选择版本', coerce=int, default=1)
    submit = SubmitField('确认部署')
    
    def __init__(self, *args, **kwargs):
        super(CreateDeployForm, self).__init__(*args, **kwargs)
        self.deploy_project.choices = [(deploy_pro.id, deploy_pro.name) for deploy_pro in Deploy.query.order_by(Deploy.name).all()] 
        self.deploy_ip.choices = [(deploy_ip.id, deploy_ip.name) for deploy_ip in Deploy.query.order_by(Deploy.name).all()] 
        self.deploy_version.choices = [(deploy_ver.id, deploy_ver.name) for deploy_ver in Deploy.query.order_by(Deploy.name).all()] 
