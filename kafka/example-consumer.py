#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import time
from kafka import KafkaConsumer 
consumer = KafkaConsumer('black_t', group_id = 'consumer-black', bootstrap_servers='127.0.0.1:9092')

def log(str):#打印日志
    t = time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())  
    print("[%s]%s"%(t,str))
    log('start consumer')

for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" %(msg.topic,msg.partition,msg.offset,msg.key,msg.value)
    log(recv)
