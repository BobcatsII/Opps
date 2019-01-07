# -*- coding: utf-8 -*-

import os
import uuid
import datetime

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import current_app, request, url_for, redirect, flash
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from opps.extensions import db
from opps.models import User, Version, Config
from opps.settings import Operations



def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)

    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False

    db.session.commit()
    return True

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

def get_conf_file_path(version,project=''):
    conf_file_dir = current_app.config['CONF_FILE_DIR'] + '/' + version + '/' + project
    return conf_file_dir

def save_files(project,module,conf_text,version):
    files_dir = get_conf_file_path(version, project)
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
    conf_file=files_dir + '/' + module
    with open('%s'%conf_file,'wb') as f:
        f.write(conf_text.encode('utf-8'))

def get_files(project,module,version):
    filepath = get_conf_file_path(version, project)
    filetext = os.path.join(filepath, module)
    with open('{0}'.format(filetext), 'r') as f:
        lines = f.readlines()
    return lines 
