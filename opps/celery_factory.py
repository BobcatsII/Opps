#-*- coding:utf8 -*-

import os
from flask import Flask
from celery import Celery
from opps.extensions import db
from opps.settings import config

def create_celery_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('opps')
    app.config.from_object(config[config_name])
    register_celery_db(app)
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def register_celery_db(app):
    db.init_app(app)
