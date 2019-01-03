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
    OPPS_MANAGE_USER_PER_PAGE = 30
    DEPLOY_ITEM_PER_PAGE = 5
    VERSIONS_PER_PAGE = 5
    HOSTS_PER_PAGE = 5
    PROJECTS_PER_PAGE = 5
    CONFIG_ITEM_PER_PAGE = 5
    CONF_FILE_DIR = os.path.join("/data/deploy","config_file")
    UPLODE_FILE_DIR = os.path.join("/data/deploy","upload_file")
    DEPLOY_LOGS_DIR = os.path.join(basedir+'/opps/logs')
    MAX_CONTENT_LENGTH = 80 * 1024 * 1024

    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = UPLODE_FILE_DIR + '/*, ' + '.war, .jar'
    DROPZONE_MAX_FILE_SIZE = 500
    DROPZONE_MAX_FILES = 8
    DROPZONE_ENABLE_CSRF = True
    DROPZONE_DEFAULT_MESSAGE = "将文件拖拽至此处 (单次上传最大数量: 8)"
    DROPZONE_INVALID_FILE_TYPE = "只允许JAR/WAR包"
    DROPZONE_FILE_TOO_BIG = "文件大小:{{filesize}}MB 文件最大限制:{{maxFilesize}}MB"
    DROPZONE_MAX_FILE_EXCEED = "上传文件已至最大数量"
    DROPZONE_UPLOAD_MULTIPLE = False
    DROPZONE_SERVER_ERROR = "Server Error:{{statusCode}}"
    DROPZONE_BROWSER_UNSUPPORTED = "您的浏览器不支持拖放文件上传"
    
    DEPLOY_DIR = "/opt/scripts/deploy"
    
    #CELERY_BROKER_URL = "amqp://linan:linan123@192.168.227.128:5672/linanhost"
    #CELERY_RESULT_BACKEND = "amqp://linan:linan123@192.168.227.128:5672/linanhost"
    CELERY_BROKER_URL = "amqp://linan:linan123@127.0.0.1:5672/linanhost"
    CELERY_RESULT_BACKEND = "amqp://linan:linan123@127.0.0.1:5672/linanhost"
#    CELERY_BROKER_URL = "redis://192.168.227.128:6879/0"
#    CELERY_RESULT_BACKEND = "redis://192.168.227.128:6879/0"

    #项目所属类型
    SYSTEM = [
               ('conf','conf'),
               ('app','app')
             ]
    #配置文件名称
    MODULE = [
                 ('config.py','config.py'), 
                 ('start_sss.py','start_sss.py')
             ]


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
