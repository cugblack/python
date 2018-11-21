#!/usr/binn/env python
# -*- coding: utf-8 -*-
from kubernetes import client, config

SERVICE_NAME = "nginx-1"

def create_service_object():
    spec = client.V1ServiceSpec(
        cluster_ip="10.109.222.57",
        ports=client.V1ServicePort(name="nginx", port="81", protocol="TCP", target_port="81"),
        selector={"app": "nginx"}
    )
    service = client.V1APIService(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=SERVICE_NAME, namespace="kafka", labels={"app": "nginx"}),
        spec=spec)
    return service

def create_service(api, service):
    api_response = api.create_namespaced_service(
        body=service,
        namespace="default"
    )
    print("Service created. status='%s'" % str(api_response.status))

def main():
    config.load_kube_config()
    extensions_v1 = client.CoreV1Api()
    service = create_service_object()
    create_service(extensions_v1, service)

if __name__ == '__main__':
    main()