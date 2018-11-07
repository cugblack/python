#!/usr/binn/env python
# -*- coding: utf-8 -*-
#仅适用于linux系统  apt-get install -y nmap
#pip install python nmap python-nmap

import sys, nmap
#获取hosts及port
SCAN_ROW = []
INPUT_DATA = raw_input("请输入host以及端口： ")
SCAN_ROW = INPUT_DATA.split(" ")
if len(SCAN_ROW) != 2:
    print "Err input, example 192.168.0.1 22"
    sys.exit(0)
hosts = SCAN_ROW[0]
port = SCAN_ROW[1]

try:
    #创建端口扫描对象
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print "Nmap not found", sys.exec_info()[0]
    sys.exit(0)
except:
    print "Unexpected error: ", sys.exec_info()[0]
    sys.exit(0)
try:
    #调用扫描方法
    nm.scan(hosts=hosts, arguments=' -v -sS -p ' + port)
except Exception, e:
    print "scan error: " + str(e)
#遍历主机
for host in nm.all_hosts():
    print "-------------------"
    print "HOST: %s (%s)" % (host, nm[host].hostname())
    print "State: %s" % nm[host].state
#遍历协议
for proto in nm[host].all_protocols():
    print "-------------------"
    print "Protocol: %s" % proto
    #遍历端口、输出端口与状态
    lport = nm[host][proto].keys()
    lport.sort()
    for port in lport:
        print "port: %s\tstate : %s" % (port, nm[host][proto][port]['state'])

#程序输出为：
'''
请输入host以及端口： 192.168.20.90 22
-------------------
HOST: 192.168.20.90 (test1)
State: <bound method PortScannerHostDict.state of {'status': {'state': 'up', 'reason': 'localhost-response'}, 'hostnames': [{'type': 'PTR', 'name': 'test1'}], 'vendor': {}, 'addresses': {'ipv4': '192.168.20.90'}, 'tcp': {22: {'product': '', 'state': 'open', 'version': '', 'name': 'ssh', 'conf': '3', 'extrainfo': '', 'reason': 'syn-ack', 'cpe': ''}}}>
-------------------
Protocol: tcp
port: 22	state : open
'''