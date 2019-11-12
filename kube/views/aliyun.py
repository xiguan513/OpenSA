#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""


import kubernetes
from django.shortcuts import HttpResponse,render
from users import models as usersModels
from kube.models import Release
from opensa.api import LoginPermissionRequired
from django.views.generic import View
from django.conf import settings
import re


def index(request):
    projects = usersModels.Project.objects.all()
    print(projects)
    return render(request,'kube/aliyun-index.html',context={"projects":projects})


class deoloy(LoginPermissionRequired,View):
    def post(self, request):
        """
        :param envName: 运行环境(YNSY)
        :param branchName: 分支信息
        :return: 返回更新服务列表
        """
        envName = request.POST.get("envName")
        branchName = request.POST.get("branchName")
        kubernetes.config.load_kube_config(config_file=settings.BASE_DIR+"/"+envName)
        v1 = kubernetes.client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for name in Release.objects.filter(branch_env=branchName,status="latest"):
            p = re.compile(r'%s-deployment-\w.*-\w.*' % name)
            for pod in ret.items:
                print(p.findall(pod.metadata.name))
                # print("%s\t%s\t%s\t%s" % (pod.status.pod_ip, pod.metadata.namespace, pod.metadata.name,pod.spec.containers[0].image))
            return HttpResponse("success")