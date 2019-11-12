#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

app_name = 'deploy'

from django.urls import path
from kube.views import deploy,index,freeze,aliyun
urlpatterns = [
    path('pod-list/<str:namespace>/',deploy.listPod.as_view(),name='pod_list'),
    path('deoloy-ment/',deploy.deoloyMent.as_view(),name='deoloy_ment'),
    path('generate-k8s/',deploy.generateK8s,name='generate_k8s'),
    path('freeze/',freeze.freeZe,name='freeze'),
    path('freeze-run/',freeze.freezRun,name='freeze_run'),
    path('aliyun/',aliyun.index,name='aliyun'),
    path('aliyun-deploy/',aliyun.deoloy.as_view(),name='aliyun_deploy'),
    path('index/',index.index),
]
