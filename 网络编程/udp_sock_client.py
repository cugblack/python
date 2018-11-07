#!/usr/binn/env python
# -*- coding: utf-8 -*-
#UDP SOCKET
from socket import *

HOST = "192.168.10.2"
PORT = 10990
BUFSIZE = 1024
ADDR = (HOST, PORT)

udpCliSock = socket(AF_INET, SOCK_DGRAM)
# udpCliSock.bind(ADDR)

try:
    while True:
        data = raw_input("> ")
        if not data:
            break
        #发送消息 data 给ADDR服务端
        udpCliSock.sendto(data, ADDR)
        data, ADDR = udpCliSock.recvfrom(BUFSIZE)
        if not data:
            break
        print data
#如果需要无限发送消息，注释掉close()函数即可
#如果close函数未注释，则只发送一次消息就退出循环
#        udpCliSock.close()
#    udpCliSock.close()
except error as e:
    print e