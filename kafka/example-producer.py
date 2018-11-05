#!/usr/bin/env pyhon
from kafka import KafkaProducer
import config
producer = KafkaProducer(bootstrap_servers = config.BOOTSTRAP_SERVERS)

def Producer():
    for i in range(10):
      producer.send('black', b'test-message')
      print i
      i = i + 1
if __name__ == '__main__':
    Producer()
