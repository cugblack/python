#!/usr/binn/env python
# -*- coding: utf-8 -*-
# import socket
from sock_server import *
from time import ctime

HOST = ""
PORT = 10990
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
try:
  while True:
    print "wait to connection..."
    tcpCliSock, addr = tcpSerSock.accept()
    print "connected from :", addr

    while True:
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        tcpCliSock.send("[%s] %s" % (ctime(),data))
        print data
#如果需要关闭连接，可以调用以下close()函数
#        tcpCliSock.close()
#  tcpSerSock.close()
except Exception as e:
  print e
