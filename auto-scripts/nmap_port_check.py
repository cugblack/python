#!/usr/binn/env python
# -*- coding: utf-8 -*-
#端口扫描
import sys, nmap

SCAN_ROW = []
INPUT_DATA = raw_input("请输入host以及端口： ")
SCAN_ROW = INPUT_DATA.split(" ")
if len(SCAN_ROW) != 2:
    print "Err input, example 192.168.0.1 22"
    sys.exit(0)

hosts = SCAN_ROW[0]
port = SCAN_ROW[1]

def port_check(hosts,port):
    try:
        #创建扫描对象
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print "Nmap not found", sys.exec_info()[0]
        sys.exit(0)
    except:
        print "Unexpected error: ", sys.exec_info()[0]
        sys.exit(0)
    try:
        #调用扫描方法
        nm.scan(hosts=hosts, arguments=' -v -sS -p ' + PORT)
    except Exception, e:
        print "scan error: " + str(e)
    #遍历扫描主机
    for host in nm.all.hosts:
        print "-------------------"
        print "HOST: %s" % (host, nm[host].hostname())
        print "State: %s" % nm[host].state
    #遍历扫描协议
    for proto in nm[host].all_protocols():
        print "-------------------"
        print "Protocol: %s" % proto

        lport = nm[host][proto].keys()
        lport.sort()
        #遍历端口、输出端口与状态
        for port in lport:
            print "port: %s\tstate : %s" % (port, nm[host][proto][port]['state'])

def main():
    port_check(hosts,port)

if __name__ == "__main__":
    main()
