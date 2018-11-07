#!/usr/binn/env python
# -*- coding: utf-8 -*-
from socket import *

HOST = "192.168.10.2"
PORT = 10990
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
try:
  while True:
    data = raw_input("> ")
    if not data:
        break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        break
    print data
except Exception as e:
    print e
