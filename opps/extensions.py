# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_dropzone import Dropzone
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_moment import Moment
from flask_avatars import Avatars
from flask_celery import Celery
#from celery import Celery

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
dropzone = Dropzone()
csrf = CSRFProtect()
mail = Mail()
moment = Moment()
avatars = Avatars()
celery = Celery()
#celery = Celery('opps', broker="amqp://linan:linan123@192.168.227.128:5672/linanhost", backend="amqp://linan:linan123@192.168.227.128:5672/linanhost")
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@login_manager.user_loader
def load_user(user_id):
    from opps.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):

    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest
