#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

app_name = 'deploy'

from django.urls import path
from kube.views import deploy
urlpatterns = [
    path('pod-list/<str:namespace>/',deploy.listPod.as_view(),name='pod_list'),
]
