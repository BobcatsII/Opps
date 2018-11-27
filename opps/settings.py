# -*- coding:utf-8 -*-

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Ops Admin', MAIL_USERNAME)
    OPPS_UPLOAD_PATH = os.path.join(basedir+'/opps/static', 'uploads')
    OPPS_MAIL_SUBJECT_PREFIX = '[Ops]'
    AVATARS_SAVE_PATH = os.path.join(OPPS_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)
    BOOTSTRAP_SERVE_LOCAL = True
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    OPPS_MANAGE_USER_PER_PAGE = 30
    DEPLOY_ITEM_PER_PAGE = 5
    VERSIONS_PER_PAGE = 5


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:tysxwg07@192.168.23.71:3306/ops?charset=utf8"


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:linan123@192.168.277.128:3306/ops?charset=utf8"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
