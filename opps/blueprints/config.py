#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.config import CreateConfigForm
from opps.extensions import db
from opps.models import Config, Project, Version

config_bp = Blueprint('config', __name__)

@config_bp.route('/')
#@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['CONFIG_ITEM_PER_PAGE']
    pagination = Config.query.order_by(Config.timestamp.desc()).paginate(page, per_page=per_page)
    config_pages = pagination.items
    return render_template('config/index.html', page=page, pagination=pagination, config_pages=config_pages)


@config_bp.route('/create', methods=['GET', 'POST'])
#@login_required
def create():
    form = CreateConfigForm()
    if request.method == "GET":
        item_name = Project.query.filter_by(project_stat=1)
        conf_file = sorted(current_app.config['MODULE'])
        conf_version = Version.query.filter().order_by('deploy_version')
        return render_template('config/config_create.html', item_name=item_name, conf_file=conf_file, conf_version=conf_version) 
    


