#!/usr/binn/env python
# -*- coding: utf-8 -*-
from kubernetes import client, config, watch

def list_pods():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def list_services():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing All services with their info:\n")
    ret = v1.list_service_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s \t%s \t%s \t%s \t%s \n" % (
        i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports))

def list_namespaces():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("List Namespaces: ")
    for ns in v1.list_namespace().items:
        print(ns.metadata.name)

def watch_namespaces():
     # Configs can be set in Configuration class directly or using helper
     # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    v1 = client.CoreV1Api()
    count = 10
    w = watch.Watch()
    for event in w.stream(v1.list_namespace, timeout_seconds=10):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        count -= 1
        if not count:
            w.stop()
        print("Ended.")

def api_version():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    print("Supported APIs (* is preferred version):")
    print("%-20s %s" %
          ("core", ",".join(client.CoreApi().get_api_versions().versions)))
    for api in client.ApisApi().get_api_versions().groups:
        versions = []
        for v in api.versions:
            name = ""
            if v.version == api.preferred_version.version and len(
                    api.versions) > 1:
                name += "*"
            name += v.version
            versions.append(name)
        print("%-40s %s" % (api.name, ",".join(versions)))


def main():
    list_services()
    list_namespaces()
    list_pods()
    watch_namespaces()
    api_version()


if __name__ == '__main__':
    main()