#-*- coding:utf-8 -*-

import os
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint
from flask_login import current_user, login_required

from opps.extensions import db


@user_bp.route('/deploy/create', methods=['GET', 'POST'])
@login_required
@confirm_required
def create_deploy():
    
    
