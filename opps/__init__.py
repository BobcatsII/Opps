# -*- coding: utf-8 -*-

import os
import click
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from opps.blueprints.auth import auth_bp
from opps.blueprints.main import main_bp
from opps.blueprints.user import user_bp
from opps.blueprints.admin import admin_bp
from opps.extensions import bootstrap, db, login_manager, dropzone, csrf, mail, moment, avatars
from opps.models import Role, User, Permission
from opps.settings import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('opps')
    
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    moment.init_app(app)
    avatars.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    #app.register_blueprint(admin_bp, url_prefix='/deploy')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)



def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除后创建.')
    def initdb(drop):
        """初始化数据库."""
        if drop:
            click.confirm('此操作将删除数据库，是否要继续?', abort=True)
            db.drop_all()
            click.echo('删除表.')
        db.create_all()
        click.echo('数据库初始化完成.')

    @app.cli.command()
    def init():
        """Initialize Opps."""
        click.echo('正在初始化数据库...')
        db.create_all()

        click.echo('正在初始化角色和权限...')
        Role.init_role()

        click.echo('完成.')
