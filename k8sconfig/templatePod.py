#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""


class TemplatePod:
    def __init__(self,**kwargs):
        self.kwargs = kwargs
    def deployment(self):
        return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": self.kwargs["image_gitname"]+"-deployment",
            "namespace": self.kwargs["namespace"],
            "labels": {
                "app": self.kwargs["image_gitname"]
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": self.kwargs["image_gitname"]
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": self.kwargs["image_gitname"]
                    }
                },
                "spec": {
                    "volumes": [
                        {
                            "name": "data",
                            "persistentVolumeClaim": {
                                "claimName": "nfs-ynsysit-pvc"
                            }
                        }
                    ],
                    "restartPolicy": "Always",
                    "imagePullSecrets": [
                        {
                            "name": self.kwargs["harbor"]
                        }
                    ],
                    "containers": [
                        {
                            "name": self.kwargs["image_gitname"],
                            "imagePullPolicy": "Always",
                            "image": self.kwargs["image_name"],
                            "resources": {
                                "requests": {
                                    "memory": "1024Mi",
                                    "cpu": "500m"
                                },
                                "limits": {
                                    "memory": "2048Mi",
                                    "cpu": "500m"
                                }
                            },
                            "command": [
                                self.kwargs["image_com"]
                            ],
                            "args": [
                                self.kwargs["image_arg"]
                            ],
                            "volumeMounts": [
                                {
                                    "name": "data",
                                    "mountPath": "/data/"
                                }
                            ],
                            "envFrom": [
                                {
                                    "configMapRef": {
                                        "name": self.kwargs["configmap"]
                                    }
                                }
                            ],
                            "ports": [
                                {
                                    "containerPort": self.kwargs["immage_port"],
                                    "name": "httpd",
                                    "protocol": "TCP"
                                }
                            ],
                            "livenessProbe": {
                                "httpGet": {
                                    "path": self.kwargs["image_path"],
                                    "port": self.kwargs["immage_port"],
                                    "scheme": "HTTP"
                                },
                                "initialDelaySeconds": 420,
                                "periodSeconds": 15,
                                "timeoutSeconds": 5
                            },
                            "readinessProbe": {
                                "tcpSocket": {
                                    "port": self.kwargs["immage_port"]
                                },
                                "initialDelaySeconds": 420,
                                "timeoutSeconds": 5,
                                "periodSeconds": 15
                            }
                        }
                    ]
                }
            }
        }
        }

