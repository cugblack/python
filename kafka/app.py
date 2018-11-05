#!/usr/bin/env python
import config
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

#BOOTSTRAP_SERVERS='127.0.0.1:9092'
kafka_host=config.KAFKA_HOST # host
kafka_port=config.KAFKA_PORT # port

def run():
    try:
        producer = KafkaProducer(bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
        kafka_host=kafka_host,
        kafka_port=kafka_port
        )])
        message_string = 'some message'
        kafka_topic = 'black'
        response = producer.send(kafka_topic, message_string.encode('utf-8'))
    except  KafkaError :
        print KafkaError
    
if __name__ == '__main__':
      run()
