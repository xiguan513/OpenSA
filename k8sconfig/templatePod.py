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
            "name": self.kwargs["gitName"]+"-deployment",
            "labels": {
                "app": self.kwargs["gitName"]
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": self.kwargs["gitName"]
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": self.kwargs["gitName"]
                    }
                },
                "spec": {
                    "restartPolicy": "Always",
                    "imagePullSecrets": [
                        {
                            "name": self.kwargs["harbor"]
                        }
                    ],
                    "containers": [
                        {
                            "name": self.kwargs["gitName"],
                            "imagePullPolicy": "Always",
                            "image": self.kwargs["imageName"],
                            "resources": {
                                "requests": {
                                    "memory": self.kwargs["requestsMem"],
                                    "cpu": self.kwargs["requestsCpu"]
                                },
                                "limits": {
                                    "memory": self.kwargs["limitsMem"],
                                    "cpu": self.kwargs["rlimitsCpu"]
                                }
                            },
                            "command": [
                                self.kwargs["common"]
                            ],
                            "args": self.kwargs["args"],
                            "envFrom": [
                                {
                                    "configMapRef": {
                                        "name": self.kwargs["configmap"]
                                    }
                                }
                            ],
                            "ports": [
                                {
                                    "containerPort": self.kwargs["port"],
                                    "name": "httpd",
                                    "protocol": "TCP"
                                }
                            ],
                            "livenessProbe": {
                                "httpGet": {
                                    "path": self.kwargs["path"],
                                    "port": self.kwargs["port"],
                                    "scheme": "HTTP"
                                },
                                "initialDelaySeconds": self.kwargs["initialDelaySeconds"],
                                "periodSeconds": self.kwargs["periodSeconds"],
                                "timeoutSeconds": self.kwargs["timeoutSeconds"]
                            },
                            "readinessProbe": {
                                "tcpSocket": {
                                    "port": self.kwargs["port"]
                                },
                                "initialDelaySeconds": self.kwargs["initialDelaySeconds"],
                                "timeoutSeconds": self.kwargs["periodSeconds"],
                                "periodSeconds": self.kwargs["timeoutSeconds"]
                            }
                        }
                    ]
                }
            }
        }
        }
    def deploymentStor(self):
        return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": self.kwargs["gitName"]+"-deployment",
            "labels": {
                "app": self.kwargs["gitName"]
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": self.kwargs["gitName"]
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": self.kwargs["gitName"]
                    }
                },
                "spec": {
                    "volumes": [
                        {
                            "name": self.kwargs['storName'],
                            "persistentVolumeClaim": {
                                "claimName": self.kwargs['claimName']
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
                            "name": self.kwargs["gitName"],
                            "imagePullPolicy": "Always",
                            "image": self.kwargs["imageName"],
                            "resources": {
                                "requests": {
                                    "memory": self.kwargs["requestsMem"],
                                    "cpu": self.kwargs["requestsCpu"]
                                },
                                "limits": {
                                    "memory": self.kwargs["limitsMem"],
                                    "cpu": self.kwargs["rlimitsCpu"]
                                }
                            },
                            "command": [
                                self.kwargs["common"]
                            ],
                            "args": [
                                self.kwargs["args"]
                            ],
                            "volumeMounts": [
                                {
                                    "name": self.kwargs['storName'],
                                    "mountPath": self.kwargs['mountPath']
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
                                    "containerPort": self.kwargs["port"],
                                    "name": "httpd",
                                    "protocol": "TCP"
                                }
                            ],
                            "livenessProbe": {
                                "httpGet": {
                                    "path": self.kwargs["path"],
                                    "port": self.kwargs["port"],
                                    "scheme": "HTTP"
                                },
                                "initialDelaySeconds": self.kwargs["initialDelaySeconds"],
                                "periodSeconds": self.kwargs["periodSeconds"],
                                "timeoutSeconds": self.kwargs["timeoutSeconds"]
                            },
                            "readinessProbe": {
                                "tcpSocket": {
                                    "port": self.kwargs["port"]
                                },
                                "initialDelaySeconds": self.kwargs["initialDelaySeconds"],
                                "timeoutSeconds": self.kwargs["periodSeconds"],
                                "periodSeconds": self.kwargs["timeoutSeconds"]
                            }
                        }
                    ]
                }
            }
        }
        }

