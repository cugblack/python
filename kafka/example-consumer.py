#!/usr/bin/env python
#-*- coding: utf-8 -*- 
from kafka import KafkaConsumer, TopicPartition

import config, time

consumer = KafkaConsumer('black', group_id = 'consumer-black', bootstrap_servers = config.BOOTSTRAP_SERVERS, onsumer_timeout_ms = 1000)

def log(str):#打印日志
    t = time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())
    print("[%s]%s"%(t,str))
    log('start consumer')

for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" %(msg.topic,msg.partition,msg.offset,msg.key,msg.value)
    log(recv)
