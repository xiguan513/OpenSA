#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

import urllib3
urllib3.disable_warnings()
import os
try:
    import ConfigParser as conf
except ImportError as e:
    import configparser as conf
import kubernetes.client
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = conf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf/autoconfig.ini'))


class K8sInt:
    def __init__(self):
        self.APISERVER = config.get('kubernetes', 'url')
        self.Token = config.get('kubernetes', 'token')
        self.configuration = kubernetes.client.Configuration()
        self.configuration.host = self.APISERVER
        self.configuration.api_key = {"authorization": "Bearer " + self.Token}
        self.configuration.verify_ssl = False
        kubernetes.client.Configuration.set_default(self.configuration)



class K8sOpt(K8sInt):
    def __init__(self,namespace):
        super(K8sOpt,self).__init__()
        self.namespace = namespace

    def create_deployment(self,deployment):
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
        #Create deployement
        api_response = api_instance.create_namespaced_deployment(
            namespace=self.namespace,
            body=deployment,
            pretty=True)
        return "Deployment created. status='%s'" % str(api_response.status)

    def update_deployment(self,MetadataName,deployment,imageName):
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
        # Update container image
        deployment['spec']['template']['spec']['containers'][0]['image'] = imageName
        print(deployment)
        # Update the deployment
        api_response = api_instance.patch_namespaced_deployment(
            name=MetadataName,
            namespace=self.namespace,
            body=deployment,
            pretty=True)
        return "Deployment updated. status='%s'" % str(api_response.status)

    def delete_deployment(self,MetadataName):
        # Delete deployment
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
        api_response = api_instance.delete_namespaced_deployment(
            name=MetadataName,
            namespace=self.namespace,
            body=kubernetes.client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5),
            pretty=True)
        return "Deployment deleted. status='%s'" % str(api_response.status)

    def list_deployment(self):
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        api_response = api_instance.list_namespaced_pod(self.namespace,watch=False)
        return api_response


if __name__ == '__main__':
    k8s = K8sOpt(namespace='ynsysit')
    import os
    from conf.templatePod import TemplatePod
    from django.db import connection

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Depovs.settings")


    class DbOpt:
        def __init__(self):
            pass

        @staticmethod
        def get_corsor():
            return connection.cursor()


    sql = """
    SELECT immage_port,
        namespace,
        configmap,
        harbor,
        image_com,
        image_arg,
        image_path
    FROM
        templatepod where tag = 'war'
    """

    a = DbOpt.get_corsor()
    a.execute(sql)
    a = a.fetchall()[0]

    bdict = {"immage_port": a[0],
             "namespace": a[1],
             "configmap": a[2],
             "harbor": a[3],
             "image_com": a[4],
             "image_arg": a[5],
             "image_path": a[5],
             "image_gitname": 'b2btest',
             "image_name": 'harbor.ynsy.com/lvyou/b2b64_c429f1:latest',
             }

    b2b = TemplatePod(**bdict)
    data = b2b.pod()
    # k8s.create_deployment(data)
    # k8s.delete_deployment('b2btest-deployment')
    # imageName = 'nginx:1.9.1'
    # k8s.update_deployment('b2btest-deployment',data,imageName)
    print("IP\tNameSpace\tName\tStatus\tNODE")
    for pod in k8s.list_deployment().items:
        print("%s\t%s\t%s\t%s\t%s" %
              (pod.status.pod_ip,pod.metadata.namespace,pod.metadata.name,pod.status.phase,pod.status.host_ip))
