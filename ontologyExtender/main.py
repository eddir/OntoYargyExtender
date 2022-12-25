import logging
from json import dumps, loads

from kafka import KafkaConsumer, KafkaProducer
import threading

# setup logging
logging.basicConfig()


def kafka_loop():
    # producer = KafkaProducer(bootstrap_servers='kafka:9092',
    #                          value_serializer=lambda x: dumps(x).encode('utf-8'),
    #                          api_version=(0, 10, 1)
    #                          )
    # producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    # msg = json.dumps({"status": True})  # update your message here
    # future = producer.send(topic, msg.encode('utf-8'))
    # result = future.get(timeout=60)
    # metrics = producer.metrics()
    # print(metrics)
    consumer = KafkaConsumer(
        'fill_ontologies',
        bootstrap_servers=['kafka:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=None,
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        api_version=(0, 10, 1)
    )
    # Read and print message from consumer
    for msg in consumer:
        logging.info("Received message: {}".format(msg.value))


if __name__ == '__main__':
    logging.info("Starting kafka loop")
    kafka_loop()
