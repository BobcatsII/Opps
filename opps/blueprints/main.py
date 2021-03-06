#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint, send_from_directory
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import func
from opps.decorators import admin_required, permission_required
from opps.extensions import db
from opps.models import User
from opps.forms.auth import LoginForm
from opps.decorators import confirm_required, permission_required
from opps.utils import redirect_back, flash_errors
from opps.models import Project, Version, Config, Hosts, DeployLog

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
@permission_required('BROWSE')
def index():
    if current_user.is_authenticated: 
        #项目统计
        project_count = Project.query.count()
        project_enable = Project.query.filter_by(project_stat=1).count()
        project_disable = Project.query.filter_by(project_stat=0).count()
        #文件配置页
        config_count = Config.query.count()
        #版本统计
        version_count = Version.query.count()
        #主机统计
        host_count = Hosts.query.count()
        #部署统计
        deploy_count = DeployLog.query.count()
        deploy_app = DeployLog.query.filter_by(dply_type='app').count()
        deploy_conf = DeployLog.query.filter_by(dply_type='conf').count()
        return render_template('main/index.html', project_count=project_count, project_enable=project_enable, project_disable=project_disable, config_count=config_count, 
                                version_count=version_count, host_count=host_count, deploy_count=deploy_count, deploy_app=deploy_app, deploy_conf=deploy_conf)
    else:
        return redirect(url_for('auth.login'))

@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
