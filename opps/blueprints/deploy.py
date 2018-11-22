#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.deploy import CreateDeployForm
from opps.extensions import db
#from opps.models import User

deploy_bp = Blueprint('deploy', __name__)


@deploy_bp.route('/')
def index():
    return render_template('deploy/index.html')

@deploy_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateDeployForm()
    if form.validate_on_submit():
        project = form.deploy_project.data
        ip = form.deploy_ip.data
        version = form.deploy_version
        if not project or not ip or not version:
            flash('缺少参数,请确认参数','warning')
        else:
            db.session.commit()
            flash('部署信息已提交', 'success')
            return redirect(url_for('.index'))
    return render_template('deploy/create_deploy.html', form=form)
