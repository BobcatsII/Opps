#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.config import CreateConfigForm
from opps.extensions import db
from opps.models import Config, Project, Version
from opps.utils import get_conf_file_path, save_files, get_files

config_bp = Blueprint('config', __name__)

@config_bp.route('/')
#@login_required
def index():
    form = CreateConfigForm()
    print (form.submit)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['CONFIG_ITEM_PER_PAGE']
    pagination = Config.query.order_by(Config.timestamp.desc()).paginate(page, per_page=per_page)
    config_pages = pagination.items
    return render_template('config/index.html', page=page, pagination=pagination, config_pages=config_pages)

@config_bp.route('/create', methods=['GET', 'POST'])
#@login_required
def create():
    form = CreateConfigForm()
    if form.validate_on_submit():
        names = form.item_name.data
        files = form.conf_file.data
        versions = form.conf_version.data
        users = form.conf_user.data
        text = form.conf_text.data 
        config = Config(item_name=names, conf_file=files, conf_version=versions, conf_user=users)
        db.session.add(config)
        db.session.commit()
        flash('配置已提交','success')
        return redirect(url_for('.index')) 
    return render_template('config/config_create.html', form=form)


