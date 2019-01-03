#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required
from opps.forms.host import HostForm
from opps.extensions import db
from opps.models import Hosts

host_bp = Blueprint('host', __name__)

@host_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['HOSTS_PER_PAGE']
    pagination = Hosts.query.order_by(Hosts.timestamp.desc()).paginate(page, per_page=per_page)
    host_pages = pagination.items
    return render_template('host/index.html', page=page, pagination=pagination, host_pages=host_pages)


@host_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = HostForm()
    if form.validate_on_submit():
        host = form.host.data
        host_type = form.host_type.data
        host = Hosts(host=host, host_type=host_type)
        db.session.add(host)
        db.session.commit()
        flash('主机信息已提交', 'success')
        return redirect(url_for('.index'))
    return render_template('host/add_host.html', form=form)
 
