#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.version import VersionForm
from opps.extensions import db
from opps.models import Version

version_bp = Blueprint('version', __name__)

@version_bp.route('/')
#@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['VERSIONS_PER_PAGE']
    pagination = Version.query.order_by(Version.timestamp.desc()).paginate(page, per_page=per_page)
    version_pages = pagination.items
    return render_template('version/index.html', page=page, pagination=pagination, version_pages=version_pages)


@version_bp.route('/create', methods=['GET', 'POST'])
#@login_required
def create():
    form = VersionForm()
    if form.validate_on_submit():
        proj_vers = form.deploy_version.data
        conf_vers = form.config_version.data
        version = Version(deploy_version=proj_vers, config_version=conf_vers)
        db.session.add(version)
        db.session.commit()
        flash('版本信息已提交', 'success')
        return redirect(url_for('.index'))
    return render_template('version/add_version.html', form=form)

