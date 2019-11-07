#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

import jenkins
import os
import sys
try:
    import ConfigParser as conf
except ImportError as e:
    import configparser as conf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = conf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.conf'))


class JenkinsOpt:
    def __init__(self):
        self.url = config.get('jenkins', 'url')
        self.user = config.get('jenkins', 'user')
        self.password = config.get('jenkins', 'password')
        self.api = jenkins.Jenkins(url=self.url,username=self.user,password=self.password)

    def buildjob(self,name,branch,envName,gitEnv,uuid):
        """
        :param name:  项目名
        :param branch: 分支
        :param envName: 构建环境
        :param gitEnv: 项目环境
        :param uuid: uuid
        :return:
        """
        self.api.build_job(name=name,parameters={'branchname':branch,"k8senv":envName,'harborpro':gitEnv,'uuid':uuid})

    def status(self,name):
        """
        :param name: job名
        :return: 返回构建的状态
        """
        num = self.api.get_job_info(name)['lastBuild']['number'] #获取最后的build号
        return num

    def joburl(self,name):
        num = self.api.get_job_info(name)['lastBuild']['number']
        print(self.api.get_build_info(name,num)['url']+"console")

    def lastbuild(self,name):
        num = self.api.get_job_info(name)['lastBuild']['number']
        print(self.api.get_build_info(name, num)['building'])

if __name__ == '__main__':
    JenkinsApi = JenkinsOpt()
    #JenkinsApi.buildjob('test', 'master', 'ynsysit', 'harbor')
    # print(JenkinsApi.status(name='test'))
    print(JenkinsApi.api.get_job_info('test'))
    # JenkinsApi.buildjob(project_name,branch_name,k8s_namespace,harborpro)
    #
    # JenkinsApi.status('test')
    #
    # JenkinsApi.joburl(project_name)
    #
    # JenkinsApi.lastbuild(project_name)