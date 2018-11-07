#!/usr/binn/env python
# -*- coding: utf-8 -*-
# UDP
from socket import *
from time import ctime

HOST = ""  # bind()所有地址
PORT = 10990
BUFSIZE = 1024  # 缓冲区1k
ADDR = (HOST, PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)
# udpSerSock.listen(5)

try:
    while True:
        #无限循环，等待消息
        print "wait for msg..."
        #接收消息、客户端地址
        data, addr = udpSerSock.recvfrom(BUFSIZE)
        #返回给客户端一个带时间信息的数据
        udpSerSock.sendto("[%s] %s" % (ctime(), data), addr)
        print "...recv from and returned to : ", addr
except error as e:
    print e
