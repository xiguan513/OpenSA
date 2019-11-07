#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""
from django.db import connection
from django.views.generic import View,ListView,DetailView,CreateView,DeleteView
from django.db.models import Q,F
from django.views.decorators.csrf import csrf_exempt
from .. import models
from Api import K8sApi,GitApi,JenkinsApi
from asset import models as assetModles
from opensa.api import LoginPermissionRequired
from django.http import HttpResponse
from django.shortcuts import redirect,reverse,render
from asset import models as assetModels
from k8sconfig.templatePod import TemplatePod
from ruamel import yaml
import os
import time
import uuid
import json
import re

class Git:
    def __init__(self,proEnv,branchName):
        """
        :param proEnv: 环境信息(erp,lvyou,lvbb)
        :param branchName: 分支信息
        """
        self.branchName = branchName
        self.proEnv = proEnv
        self.serverName = []


    def updateCheck(self):
        """
        :return: 需要更新的服务列表
        """
        gitInfoList = models.GitInfo.objects.filter(git_env__name=self.proEnv)
        # print("查询git",gitInfoList)
        for gitInfo in gitInfoList:
            repo = GitApi.GitOpt(gitInfo.git_ssh,self.branchName, gitInfo.git_name)
            repo.clone()
            # print("克隆项目 %s " % gitInfo.git_name)
            curBranch = repo.activebranch()#获取当前分支
            # print("获取分支 %s" % curBranch)
            if curBranch != self.branchName:
                #检查远程分支是否有此分支，如果没有此分支，使用master分支
                originBranch = repo.repo.git.branch('-r').split()
                if 'origin/'+self.branchName not in originBranch:
                    self.branchName = 'origin/master'
                repo.checkout(self.branchName)
                histCommit = repo.repo.head.reference.commit #获取当前commit
                repo.remotepull(self.branchName)
                nowCommit = repo.repo.head.reference.commit #获取更新以后的commit
                print(histCommit,nowCommit,gitInfo.git_name,self.branchName)
                if histCommit != nowCommit:
                    self.serverName.append(gitInfo.git_name)
        return self.serverName




class listPod(LoginPermissionRequired,View):

    def get(self,request,namespace):
        k8scon = K8sApi.K8sOpt(namespace)
        podStauts = k8scon.list_deployment()
        workEnv = assetModels.Work_Env.objects.all()

        context = {
            "select": namespace,
            "workenv_list":workEnv,
            'podStauts':podStauts.items
        }

        return render(request,'kube/kube-list.html',context=context)




class deoloyMent(LoginPermissionRequired,View):
    def get(self,request):
        workEnv = assetModels.Work_Env.objects.all()
        projectEnv = assetModles.ServerUse.objects.all()
        context = {
            "workenv_list":workEnv,
            "project_list":projectEnv,
        }
        return render(request, 'kube/kube-deploy.html', context=context)

    def post(self,request):
        """
        :param envName: 运行环境(ynsysit,ynsyuat)
        :param proEnv: 环境信息(erp,lvyou,lvbb)
        :param branchName: 分支信息
        :param all: 是否全部更新
        :return: 返回更新服务列表
        """
        envName = request.POST.get("envName")
        proEnv = request.POST.get("proEnv")
        branchName = request.POST.get("branchName")
        checkAll = request.POST.get("checkAll")
        buildPro = JenkinsApi.JenkinsOpt()
        statusName = envName+proEnv
        buildUuid = uuid.uuid4()
        status = models.DeployStatus.objects.filter(env_name=statusName).filter(~Q(renew_status='部署完成')).exists()
        if status:
            return HttpResponse("exists")
        else:
            if checkAll == "True":
                gitInfoList = models.GitInfo.objects.filter(git_env__name=proEnv)
                Git(proEnv,branchName).updateCheck()
                projectName = [project.git_name for project in gitInfoList]
                for project in projectName:
                    models.DeployStatus.objects.create(server_name=project,env_name=statusName, renew_status='开始Build',branch_env=branchName,build_uuid=buildUuid)
            else:
                projectName = [key for key in Git(proEnv, branchName).updateCheck()]
                print(projectName,'部分更新')
                proList = list(filter(
                    lambda proName: models.GitInfo.objects.values('git_sort').filter(git_name=proName)[0]['git_sort'] == 1,
                    projectName))
                if proList:
                    # print(proList, "检查到有common")
                    gitInfoList = models.GitInfo.objects.filter(git_env__name=proEnv)
                    projectName = [project.git_name for project in gitInfoList]
                for project in projectName:
                    models.DeployStatus.objects.create(server_name=project,env_name=statusName, renew_status='开始Build',branch_env=branchName,build_uuid=buildUuid)
            print("判断是否执行到projectName:%s" % projectName)
            if not projectName:
                models.DeployStatus.objects.filter(build_uuid=buildUuid).update(renew_status="没有检查到更新项目",)
                return HttpResponse("None")
            elif isinstance(projectName, list):
                for project in projectName:
                    tmpParam = models.GitInfo.objects.filter(git_name=project)
                    # print("查询对象%s" % tmpParam)
                    for parm in tmpParam:
                        try:
                            # print("实行build %s" % parm)
                            buildPro.buildjob(project,branchName,envName,proEnv,buildUuid)
                            time.sleep(10)
                        except Exception as err:
                            print(err)
                else:
                    models.DeployStatus.objects.filter(build_uuid=buildUuid).update(renew_status='Build')
            else:
                return HttpResponse("fail")
            #此处有问题
            return HttpResponse("success")

@csrf_exempt
def generateK8s(request):
    if request.method == 'POST':
        postBody = request.body
        text = json.loads(postBody.decode('utf-8'))  # linux
        # text = json.loads(postBody) # mac
        branch = text['branchname']
        gitName = text['gitname']
        imageName = text['imagename']
        nameSpace = text['k8senv']
        imagePor = text['project']
        buildUuid = text['uuid']
        envName = nameSpace + imagePor
        updateTem = models.TemplatePod.objects.filter(gitinfo__git_name=gitName).first()
        if re.findall(r'^release/\d{3}$',branch):
            #记录release版本的镜像信息
            models.Release.objects.filter(server_name=gitName,branch_env=branch).update(status="")
            models.Release.objects.create(image_name=imageName,server_name=gitName,branch_env=branch)
            # print(connection.queries)
        else:
            models.UpdateInfo.objects.create(build_uuid=buildUuid,server_name=gitName,
                                             image_name=imageName, pro_env=nameSpace,
                                             image_env=imagePor,branch_env=branch)

        deployName = gitName.replace("_", "-")
        args = updateTem.args #获取命令参数
        if ',' in args:
            args = args.split(",")
        else:
            args = updateTem.args
        if updateTem.storage: #判断是否有添加存储
            data = {"gitName": deployName,
                    "configmap": updateTem.configmap,
                    "harbor": updateTem.harbor,
                    "common": updateTem.common,
                    "args": args,
                    "path": updateTem.path,
                    "port": updateTem.port,
                    "replicas": updateTem.replicas,
                    "requestsMem": updateTem.requestsMem,
                    "requestsCpu": updateTem.requestsCpu,
                    "limitsMem": updateTem.limitsMem,
                    "rlimitsCpu": updateTem.rlimitsCpu,
                    "initialDelaySeconds": int(updateTem.initialDelaySeconds),
                    "periodSeconds": int(updateTem.periodSeconds),
                    "timeoutSeconds": int(updateTem.timeoutSeconds),
                    "imageName": imageName,
                    "storName": updateTem.storage.stroname,
                    "claimName": updateTem.storage.claimname,
                    "mountPath": updateTem.storage.mountpath,
                    }
            SerTemPod = TemplatePod(**data)
            body = SerTemPod.deploymentStor()
        else:
            data = {"gitName": deployName,
                    "configmap": updateTem.configmap,
                    "harbor": updateTem.harbor,
                    "common": updateTem.common,
                    "args": args,
                    "path": updateTem.path,
                    "port": updateTem.port,
                    "replicas": updateTem.replicas,
                    "requestsMem": updateTem.requestsMem,
                    "requestsCpu": updateTem.requestsCpu,
                    "limitsMem": updateTem.limitsMem,
                    "rlimitsCpu": updateTem.rlimitsCpu,
                    "initialDelaySeconds": int(updateTem.initialDelaySeconds),
                    "periodSeconds": int(updateTem.periodSeconds),
                    "timeoutSeconds": int(updateTem.timeoutSeconds),
                    "imageName": imageName,
                    }
            SerTemPod = TemplatePod(**data)
            body = SerTemPod.deployment()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(BASE_DIR, 'configfile/%s.yaml' % deployName), "w", encoding="utf-8") as f:
            #生产pod.yaml文件
            yaml.dump(body, f, Dumper=yaml.RoundTripDumper)
        k8s = K8sApi.K8sOpt(namespace=nameSpace)
        if k8s.read_deployment(deployName+'-deployment'):
            print("%s pod已经存在，更新pod" % deployName)
            status = k8s.update_deployment(MetadataName=deployName+'-deployment',deployment=body,imageName=imageName)
        else:
            print("没有此 %s pod创建新pod" % deployName)
            status = k8s.create_deployment(body)
        models.DeployStatus.objects.filter(build_uuid=buildUuid).update(renew_status='部署完成')
        return HttpResponse("ok")



