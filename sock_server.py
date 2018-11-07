#!/usr/binn/env python
# -*- coding: utf-8 -*-
#TCP SOCKET
from socket import *
from time import ctime

HOST = "" #bind()所有地址
PORT = 10990
BUFSIZE = 1024 #缓冲区1k
ADDR = (HOST, PORT)

#创建套接字
tcpSerSock = socket(AF_INET,SOCK_STREAM)
#监听
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)  #最大同时连接数
try:
  while True:
    print "wait to connection..."
    #进入无线循环，等待连接的接受连接
    tcpCliSock, addr = tcpSerSock.accept()
    print "connected from :", addr

    while True:
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        #返回一个带时间戳的数据
        tcpCliSock.send("[%s] %s" % (ctime(),data))
        print data
#如果需要关闭连接，可以调用以下close()函数
#        tcpCliSock.close()
#  tcpSerSock.close()
except Exception as e:
  print e
