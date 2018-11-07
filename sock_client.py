#!/usr/binn/env python
# -*- coding: utf-8 -*-
from socket import *

HOST = "192.168.10.2"
PORT = 10990
BUFSIZE = 1024
ADDR = (HOST, PORT)

#创建客户端套接字
tcpCliSock = socket(AF_INET, SOCK_STREAM)
#绑定服务器端地址
tcpCliSock.connect(ADDR)

try:
  while True:
    #进入循环，除非输入为空或服务端退出，否则一直保持连接并发送键盘输入的数据
    data = raw_input("> ")
    if not data:
        break
    tcpCliSock.send(data)
    #接收并显示服务器传回的带了时间戳的字串
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        break
    print data
except Exception as e:
    print e
