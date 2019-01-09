# -*- coding:utf-8 -*-

import os
import time
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from opps.extensions import db
from flask_avatars import Identicon

# relationship table
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                             )

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['BROWSE'],
            'User': ['BROWSE', 'UPLOAD'],
            'Moderator': ['BROWSE', 'UPLOAD', 'DEPLOY', 'MODERATE'],
            'Administrator': ['BROWSE', 'UPLOAD', 'DEPLOY', 'MODERATE', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email  = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=datetime.now)
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    avatar_raw = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)
    locked = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_avatar()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def lock(self):
        self.locked = True
        self.role = Role.query.filter_by(name='Locked').first()
        db.session.commit()

    def unlock(self):
        self.locked = False
        self.role = Role.query.filter_by(name='User').first()
        db.session.commit()

    def block(self):
        self.active = False
        db.session.commit()

    def unblock(self):
        self.active = True
        db.session.commit()

    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'


    @property
    def is_active(self):
        return self.active

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions
    
    @classmethod
    def get_username(cls, id):
        username = cls.query.get(id).username
        return username

class DeployLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dply_type = db.Column(db.String(20))
    dply_item = db.Column(db.String(50))
    dply_host = db.Column(db.String(30))
    dply_version = db.Column(db.String(20))
    dply_user = db.Column(db.String(20))
    dply_date = db.Column(db.DateTime, default=datetime.now)
    dply_stat = db.Column(db.String(20))

    @classmethod
    def get_deploy_timestamp(cls,delpoy_id):
        date = cls.query.get(delpoy_id).dply_date
        timestamp = int(time.mktime(date.timetuple()))
        return timestamp

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deploy_version = db.Column(db.String(20), unique=True, nullable=False)
    config_version = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_type = db.Column(db.String(100), nullable=False)
    project_port = db.Column(db.Integer)
    project_info = db.Column(db.String(100))
    project_stat = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    conf_version = db.Column(db.String(50), nullable=False)
    conf_file = db.Column(db.String(50), nullable=False)
    conf_user = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

class Hosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(80), nullable=False)
    host_type = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

@db.event.listens_for(User, 'after_delete', named=True)
def delete_avatars(**kwargs):
    target = kwargs['target']
    for filename in [target.avatar_s, target.avatar_m, target.avatar_l, target.avatar_raw]:
        if filename is not None:  # avatar_raw may be None
            path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
            if os.path.exists(path):  # not every filename map a unique file
                os.remove(path)
