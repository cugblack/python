#!_*_ coding=utf-8
#!/usr/bin/env python
import config, logging
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.errors import KafkaError

kafka_host=config.KAFKA_HOST # host
kafka_port=config.KAFKA_PORT # port
KAFKA_TOPIC = "test"
def Kaaka_Producer():
    try:
        producer = KafkaProducer(bootstrap_servers = ["{kafka_host}:{kafka_port}".format(
        kafka_host = kafka_host,
        kafka_port = kafka_port
        )])

        for msg in range(10):
            producer.send(KAFKA_TOPIC, b'test msg')
            print msg
        print "producer succed"
    except  KafkaError :
        print KafkaError

def Kafka_Consumer():
    try:
        consumer = KafkaConsumer(group_id = "black", bootstrap_servers = config.BOOTSTRAP_SERVERS, consumer_timeout_ms = 1000)
        consumer.assign([TopicPartition(topic=KAFKA_TOPIC, partition=0)])
        # consumer.subscribe(topics=['my_topic', 'topic_1'])#订阅多个topic
        for msg in consumer:
            print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value))
    except KafkaError:
        print KafkaError

def main():
    # tasks = [
    # #     Kaaka_Producer(),
    #       Kafka_Consumer()
    # ]
    # for t in tasks:
    #     t.start()

    # for task in tasks:
    #     task.stop()

    # for task in tasks:
    #     task.join()
    Kaaka_Producer()
    Kafka_Consumer()
if __name__ == '__main__':
    logging.basicConfig(
            format = "%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s",

            level = logging.INFO
    )
    main()
