#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

from django.http import HttpResponse


def index(request):
    print("11111")
    return HttpResponse("11111")