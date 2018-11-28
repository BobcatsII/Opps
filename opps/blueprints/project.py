#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.project import ProjectForm
from opps.extensions import db
from opps.models import Project

project_bp = Blueprint('project', __name__)

@project_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PROJECTS_PER_PAGE']
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(page, per_page=per_page)
    project_pages = pagination.items
    return render_template('project/index.html', page=page, pagination=pagination, project_pages=project_pages)


@project_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        proj_name = form.project_name.data
        proj_type = form.project_type.data
        proj_port = form.project_port.data
        proj_info = form.project_info.data
        proj_stat = form.project_stat.data
        project = Project(project_name=proj_name, project_type=proj_type, project_port=proj_port, project_info=proj_info, project_stat=proj_stat)
        db.session.add(project)
        db.session.commit()
        flash('项目信息已提交', 'success')
        return redirect(url_for('.index'))
    return render_template('project/add_project.html', form=form)

