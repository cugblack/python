#!/usr/bin/env python
import config
from kafka import kafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

#BOOTSTRAP_SERVERS='127.0.0.1:9092'
kafka_host='127.0.0.1' # host
kafka_port=9092 # port

def run():
    producer = KafkaProducer(bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
        kafka_host=kafka_host,
        kafka_port=kafka_port
    )])
    message_string = 'some message'
    kafka_topic = 'test1'
    response = producer.send(kafka_topic, message_string.encode('utf-8'))
    
if __name__ == '__main__':
      run()
