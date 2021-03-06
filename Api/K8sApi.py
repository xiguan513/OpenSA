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
config.read(os.path.join(BASE_DIR, 'config.conf'))


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


    def create_namespace(self):
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        body = {"apiVersion": 'v1',
                "kind": 'Namespace',
                "metadata": {"name": self.namespace, "labels": {"name": self.namespace}}}
        try:
            api_response = api_instance.create_namespace(body,)
            print(api_response)
        except kubernetes.client.rest.ApiException as e:
            print("Exception when calling CoreV1Api->create_namespace: %s\n" % e)

    def delete_namespace(self):
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        try:
            api_response = api_instance.delete_namespace(name=self.namespace)
        except kubernetes.client.rest.ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespace: %s\n" % e)


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
        # print(deployment)
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

    def read_deployment(self,name):
        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.read_namespaced_deployment(name, self.namespace)
            print(api_response)
            return True
        except kubernetes.client.rest.ApiException as e:
            return False


if __name__ == '__main__':
    k8s = K8sOpt(namespace='ynsysit')
    import re
    from kube.models import Release
    # k8s.read_deployment('b2b1-deployment')
    # k8s.delete_deployment('ty-ynsy-activity-deployment')
    from k8sconfig.templatePod import TemplatePod
    # k8s.create_namespace('song')
    # k8s.create_deployment(data)
    # k8s.delete_deployment('b2btest-deployment')
    # imageName = 'nginx:1.9.1'
    # k8s.update_deployment('b2btest-deployment',data,imageName)
    # print("IP\tNameSpace\tName\tStatus\tNODE")

    # for pod in k8s.list_deployment().items:
    #     #releaseInfo = Release.objects.filter(branch_env="release/145", status="latest")
    #     #print(pod.metadata.name)
    #     print(pod.status.container_statuses[0].ready)
    #     print("%s\t%s\t%s\t%s\t%s" %
    #           (pod.status.pod_ip,pod.metadata.namespace,pod.metadata.name,pod.status.phase,pod.status.host_ip))

    for name in Release.objects.filter(branch_env="release/", status="latest"):
        p = re.compile(r'%s-deployment-\w.*-\w.*' % name)
        for pod in k8s.list_deployment().items:
            print(p.findall(pod.metadata.name))
            # print("%s\t%s\t%s\t%s" % (pod.status.pod_ip, pod.metadata.namespace, pod.metadata.name,pod.spec.containers[0].image))



