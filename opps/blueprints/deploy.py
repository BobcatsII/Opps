#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.deploy import CreateDeployForm
from opps.extensions import db
from opps.models import DeployLog

deploy_bp = Blueprint('deploy', __name__)


@deploy_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['DEPLOY_ITEM_PER_PAGE']
    pagination = DeployLog.query.order_by(DeployLog.dply_date.desc()).paginate(page, per_page=per_page)
    deploy_pages = pagination.items
    return render_template('deploy/index.html', page=page, pagination=pagination, deploy_pages=deploy_pages)

@deploy_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateDeployForm()
    if form.validate_on_submit():
        user = form.deploy_user.data
        project = form.deploy_project.data
        host = form.deploy_host.data
        version = form.deploy_version.data
        deploy = DeployLog(dply_user=user, dply_item=project, 
                           dply_host=host, dply_version=version, dply_stat='部署成功')
        db.session.add(deploy)
        if not project or not host or not version:
            flash('缺少参数,请确认参数','warning')
        else:
            db.session.commit()
            flash('部署信息已提交', 'success')
            return redirect(url_for('.index'))
    return render_template('deploy/create_deploy.html', form=form)
