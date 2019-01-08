#-*- coding:utf-8 -*-

import os
import shutil
import logging
import tarfile
import subprocess
import time
from time import sleep
from opps.celery_factory import create_celery_app
from celery import platforms
from opps.extensions import db
from opps.models import DeployLog
from flask import Flask,render_template, flash, redirect, url_for, current_app, request, abort, Blueprint, jsonify

platforms.C_FORCE_ROOT = True
celery = create_celery_app()

@celery.task()
def ansible_deploy(type, project, version, ip, deploy_id, deploy_date):
    script_path = current_app.config['DEPLOY_DIR'] + '/prod_vms-deploy.sh'
    task = subprocess.getstatusoutput('bash {0} {1} {2} {3} {4} {5} > {6}/deploy/{7}.log 2>&1'.format(script_path, project, 
                                          version, ip, type, deploy_date, current_app.config['DEPLOY_LOGS_DIR'], deploy_id))
    sql = DeployLog.query.get(deploy_id)
    if task[0] == 0:
        sql.dply_stat = '部署成功'
    else:
        sql.dply_stat = '部署失败'
    db.session.commit()
    return task

@celery.task()
def ansible_rollback(type, project, version, ip, deploy_id, deploy_date, user):
    script_path = current_app.config['DEPLOY_DIR'] + '/prod_vms-rollback.sh'
    task = subprocess.getstatusoutput('bash {0} {1} {2} {3} {4} {5} > {6}/rollback/{7}.log 2>&1'.format(script_path, project, 
                                            version, ip, type, deploy_date, current_app.config['DEPLOY_LOGS_DIR'], deploy_id))
    sql = DeployLog.query.get(deploy_id)
    if task[0] == 0:
        sql.dply_stat = '回滚成功'
        sql.dply_user = user
    else:
        sql.dply_stat = '回滚失败'
    db.session.commit()
    return task

@celery.task()
def ansible_again(type, project, version, ip, deploy_id, deploy_date, user):
    script_path = current_app.config['DEPLOY_DIR'] + '/prod_vms-again.sh'
    print (script_path)
    print (type, project, version, ip, deploy_id, deploy_date, user)
    task = subprocess.getstatusoutput('bash {0} {1} {2} {3} {4} {5} > {6}/deploy/{7}.log 2>&1'.format(script_path, project,
                                          version, ip, type, deploy_date, current_app.config['DEPLOY_LOGS_DIR'], deploy_id))
    print (task)
    sql = DeployLog.query.get(deploy_id)
    print ("sqli="+sql )
    if task[0] == 0:
        sql.dply_stat = '重部成功'
        sql.dply_user = user
    else:
        sql.dply_stat = '重部失败'
    db.session.commit()
    return task

