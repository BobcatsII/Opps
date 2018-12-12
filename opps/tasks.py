#-*- coding:utf-8 -*-

import os
import shutil
import logging
import tarfile
import commands
import time
from time import sleep
from celery.decorators import task
from celery import platforms
from opps.models import DeployLog
from flask import render_template, flash, redirect, url_for, current_app, request, abort, Blueprint, jsonify


platforms.C_FORCE_ROOT = True

@task
def ansible_deploy(type,project,version,dubbo_version,ip,deploy_id,deploy_date,branch):
    env = settings.PROJECT_ENV
    script_path=settings.DEPLOY_DIR+'/'+env+'_'+'vm-deploy.sh'
    task = commands.getstatusoutput('bash %s %s %s %s %s %s %s %s > %s/deploy/%s.log 2>&1'%(script_path,env,project,version,dubbo_version,ip,branch,deploy_date,settings.LOGS_DIR,deploy_id))
    deploy = Deploy_log.objects.get(id = deploy_id)
    if task[0] == 0:
        deploy.state = u'部署成功'
    else:
        deploy.state = u'部署失败'
    deploy.save()
    return task
