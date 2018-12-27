#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint, send_from_directory
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import func


from opps.extensions import db
from opps.models import User
from opps.forms.auth import LoginForm
from opps.decorators import confirm_required, permission_required
from opps.utils import redirect_back, flash_errors
#from opps.forms.main import 

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated: 
        #项目统计
        project_count = Project.query.count()
        project_enable = Project.query.filter_by(project_stat=1).count()
        project_disable = Project.query.filter_by(project_stat=0).count()
        return render_template('main/index.html')
    else:
        return redirect(url_for('auth.login'))



@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
