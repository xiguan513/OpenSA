#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""
from django.views.generic import View,ListView,DetailView,CreateView,DeleteView
from .. import models
from Api import K8sApi,GitApi
from asset import models as assetModles
from opensa.api import LoginPermissionRequired
from django.http import HttpResponse
from django.shortcuts import redirect,reverse,render


class listPod(LoginPermissionRequired,View):
    context_object_name = 'kube_list'


    def get_context_data(self, **kwargs):
        context = {
            "kube_list": "active",
            "kube_list_active": "active",
        }

    def get(self,request,namespace):
        k8scon = K8sApi.K8sOpt(namespace)
        podStauts = k8scon.list_deployment()
        print(type(podStauts))
        context = {
            'podStauts':[podStauts.items]
        }
        # print("%s\t%s\t%s\t%s\t%s" %
        #       (pod.status.pod_ip, pod.metadata.namespace, pod.metadata.name, pod.status.phase, pod.status.host_ip))

        return render(request,'kube/kube-list.html',context=context)



class buildJob(ListView):
    pass

class createPod(View):
    pass

class updatePod(View):
    pass

class UpdateRecord(CreateView):
    pass


