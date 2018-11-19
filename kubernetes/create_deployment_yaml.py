#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
import yaml
from kubernetes import client, config, utils

def create_yaml():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.load(f)
        k8s_beta = client.ExtensionsV1beta1Api()
        resp = k8s_beta.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % str(resp.status))

def create_deployment_():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    k8s_client = client.ApiClient()
    k8s_api = utils.create_from_yaml(k8s_client, "nginx-deployment.yaml")
    deps = k8s_api.read_namespaced_deployment("nginx-deployment", "default")
    print("Deployment {0} created".format(deps.metadata.name))

def main():
    create_deployment_()

if __name__ == "__main__":
    if __name__ == '__main__':
