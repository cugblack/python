#!/usr/bin/env pyhon
from kafka import KafkaProducer 
producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')

def Producer():
    for i in range(100):
      producer.send('black_t', b'test-message')
      print i
      i = i + 1
if __name__ == '__main__':
    Producer()
