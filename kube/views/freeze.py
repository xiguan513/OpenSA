#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

from kube import models
from django.shortcuts import  HttpResponse,render,get_object_or_404,get_list_or_404
from django.http import JsonResponse,StreamingHttpResponse
from asset import models as assetModels
from Api import GitApi




def freeZe(request):
    deployList = models.Codefreeze.objects.all()
    proNames = assetModels.ServerUse.objects.all()
    return render(request,'kube/freeze.html',{"deployList":deployList,"proNames":proNames})


def freezRun(request):
    if request.method == "POST":
        checkoutBranch = request.POST.get("checkoutBranch")
        codeFreeze = request.POST.get("codeFreeze")
        projectName = request.POST.get("project")
        gitTag = request.POST.get("gitTag")
        print(checkoutBranch,codeFreeze,projectName,gitTag)
        projects = models.GitInfo.objects.filter(git_env__name=projectName)
        for project in projects:
            try:
                repo = GitApi.GitOpt(project.git_ssh,checkoutBranch,project.git_name)
                repo.checkout(checkoutBranch) #切换到需要封板的分支
                repo.remotepull(checkoutBranch) #更新最新代码
                print("项目名: %s 当前分支: %s" (project.git_name,repo.activebranch()))  #查看当前分支
                repo.createhead(codeFreeze) #创建封板分支
                repo.createtag(gitTag,gitTag)#创建封板tag
                print("项目名: %s 封板以后分支: %s"(project.git_name, repo.activebranch()))  #查看当前分支
                repo.remotepush(codeFreeze)
                repo.remotepush(gitTag)
            except Exception as err:
                print(err)
                return HttpResponse("fail")
            else:
                models.Codefreeze.objects.create(project_name=project.git_name,checkout_branch=checkoutBranch,code_freeze=codeFreeze,
                                             git_tag=gitTag)
        else:
            return HttpResponse("success")

