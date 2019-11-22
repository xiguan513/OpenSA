#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

import time
from kube import models
from opensa.celery import app as celery_app
from Api import K8sApi,GitApi,JenkinsApi
from django.http import HttpResponse




@celery_app.task
def deployCelery(envName,proEnv,branchName,buildUuid,projectName):
    buildPro = JenkinsApi.JenkinsOpt()
    for project in projectName:
        tmpParam = models.GitInfo.objects.filter(git_name=project)
        for parm in tmpParam:
            try:
                buildPro.buildjob(project, branchName, envName, proEnv, buildUuid)
                time.sleep(20)
            except Exception as err:
                return err
    else:
        models.DeployStatus.objects.filter(build_uuid=buildUuid).update(renew_status='Build')
        return "Build"
