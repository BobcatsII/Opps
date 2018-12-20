#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from opps.forms.deploy import CreateDeployForm
from opps.extensions import db
from opps.models import DeployLog, Project, Config
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
        user = form.deploy_user.data
        projects = form.deploy_project.data
        host = form.deploy_host.data
        version = form.deploy_version.data
        for project in projects.split(','):
            deploy = DeployLog(dply_type=dtype, dply_user=user, dply_item=project, dply_host=host, dply_version=version)
            db.session.add(deploy)
            db.session.commit()
            deploy_last = DeployLog.query.order_by(DeployLog.dply_date.desc()).first()
            deploy_id = deploy_last.id
            deploy_timestamp = DeployLog.get_deploy_timestamp(deploy_id)
            sql = DeployLog.query.get(deploy_id)
            sql.dply_stat = "正在部署"
            db.session.commit()
            task_id = ansible_deploy.delay(sql.dply_type, sql.dply_item, sql.dply_version, sql.dply_host, deploy_id, deploy_timestamp)
            #task_id = ansible_deploy.apply_async(args=[sql.dply_type, sql.dply_item, sql.dply_version, sql.dply_host, deploy_id, deploy_timestamp], queue='myvhost')
            #sql.celery_id = task_id
            #db.session.commit()
            flash('部署信息已提交', 'success')
            return redirect(url_for('.index'))
    return render_template('deploy/create_deploy.html', form=form)


#ajax还有点问题
@deploy_bp.route('/get_project', methods=['GET', 'POST'])
@login_required
def get_project():
    type = request.args.get('type')
    project = [ str(item_name.project_name) for item_name in  Project.query.filter_by(project_stat=1, project_type=type).order_by(Project.project_name) ]
    a=str(project)
    project = a.strip('[]').replace(' ', '')
    return jsonify(project)
        
@deploy_bp.route('/detail', methods=['GET','POST'])
@login_required
def detail():
    deploy_id = request.args.get('deploy_id')
    logtype = request.args.get('logtype')
    logs_dir = current_app.config['DEPLOY_LOGS_DIR']
    with open("{0}/{1}/{2}.log".format(logs_dir, logtype, deploy_id), "r") as fs:
        lines = fs.readlines()
    return jsonify(lines)

@deploy_bp.route('/rollback', methods=['GET', 'POST'])
@login_required
def rollback():
    pass

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
