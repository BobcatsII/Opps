#-*- coding:utf-8 -*-

import os
import time
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint, jsonify, make_response
from flask_login import current_user, login_required
from opps.forms.deploy import CreateDeployForm
from opps.extensions import db
from opps.models import DeployLog, Project, Config, User
from opps.tasks import ansible_deploy

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
        dtype = form.deploy_type.data
        if dtype == "app":
            user = form.deploy_user.data
            project = form.deploy_project_app.data
            host = form.deploy_host_app.data
            version = form.deploy_version_app.data
            deploy = DeployLog(dply_type=dtype, dply_user=user, dply_item=project, dply_host=host, dply_version=version)
            db.session.add(deploy)
            db.session.commit()
            deploy_last = DeployLog.query.order_by(DeployLog.dply_date.desc()).first()
            deploy_id = deploy_last.id
            deploy_timestamp = DeployLog.get_deploy_timestamp(deploy_id)
            sql = DeployLog.query.get(deploy_id)
            sql.dply_stat = "正在部署"
            db.session.commit()
            rsp = ansible_deploy.delay(sql.dply_type, sql.dply_item, sql.dply_version, sql.dply_host, deploy_id, deploy_timestamp)
        else:
            user = form.deploy_user.data
            project = form.deploy_project_conf.data
            host = form.deploy_host_conf.data
            version = form.deploy_version_conf.data
            deploy = DeployLog(dply_type=dtype, dply_user=user, dply_item=project, dply_host=host, dply_version=version)
            db.session.add(deploy)
            db.session.commit()
            deploy_last = DeployLog.query.order_by(DeployLog.dply_date.desc()).first()
            deploy_id = deploy_last.id
            deploy_timestamp = DeployLog.get_deploy_timestamp(deploy_id)
            sql = DeployLog.query.get(deploy_id)
            sql.dply_stat = "正在部署"
            db.session.commit()
            rsp = ansible_deploy.delay(sql.dply_type, sql.dply_item, sql.dply_version, sql.dply_host, deploy_id, deploy_timestamp)
        flash('部署信息已提交', 'success')
        return redirect(url_for('.index'))
    return render_template('deploy/create_deploy.html', form=form)

@deploy_bp.route('/detail', methods=['GET','POST'])
@login_required
def detail():
    deploy_id = request.args.get('deploy_id')
    logtype = request.args.get('logtype')
    logs_dir = current_app.config['DEPLOY_LOGS_DIR']
    with open("{0}/{1}/{2}.log".format(logs_dir, logtype, deploy_id), "r") as text_file:
        lines = text_file.readlines()
    res = make_response('{0}'.format(lines), 200)
    return res


@deploy_bp.route('/rollback', methods=['GET', 'POST'])
@login_required
def rollback():
    rollback_id = request.args.get('deploy_id')
    rollback_user = User.get_username(request.session.get('id'))
    rollback_data = DeployLog.query.get(id=deploy_id)
    rollback_project = rollback_data.dply_item
    rollback_host = rollback_data.dply_host
    rollback_version = rollback_data.dply_version
    rollback_type = Project.query.get(project_name=rollback_project).project_type
    rollback_timestamp = DeployLog.get_deploy_timestamp(deploy_id)
    rollback_data.dply_stat = "正在回滚"
    db.session.commit()
    rollback_deploy = ansible_rollback.delay(rollback_type, rollback_project, rollback_version, rollback_host, rollback_id, rollback_timestamp, rollback_user)
    flash('回滚操作已提交', 'success')
    return redirect(url_for('.index'))
    
   
@deploy_bp.route('/again', methods=['GET', 'POST'])
@login_required
def again():
    again_id = request.args.get('deploy_id')
    again_user = User.get_username(request.session.get('id'))
    again_data = DeployLog.query.get(again_id)
    again_project = again_data.dply_item
    again_host = again_data.dply_host
    again_version = again_data.dply_version
    again_type = Project.query.get(project_name=again_project).project_type
    again_deploy = DeployLog(dply_type=again_type, dply_user=again_user, dply_item=again_project, dply_host=again_host, dply_version=again_version)
    db.session.commit()
    again_id = again_deploy.id
    again_timestamp = DeployLog.get_deploy_timestamp(again_id)
    again_sql = DeployLog.query.get(again_id)
    again_sql.dply_stat = "正在重新部署"
    again_deploy = ansible_deploy.delay(again_type, again_project, again_version, again_host, again_id, again_timestamp) 
    flash('重新部署已提交', 'success')
    return redirect(url_for('.index'))

@deploy_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    filedir = current_app.config['UPLODE_FILE_DIR']
    if request.method == 'POST' and 'file' in request.files:
        upfile = request.files.get('file')
        bag = upfile.filename.split('.')[1]
        bagdir = filedir + '/' + bag
        if not os.path.exists(bagdir):
            os.makedirs(bagdir)
        upfile.save(os.path.join(bagdir, upfile.filename))
    return render_template('deploy/upload_file.html')    

