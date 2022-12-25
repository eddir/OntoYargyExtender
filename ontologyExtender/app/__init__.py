import logging
from json import loads

from app.enum import EnvironmentVariables as EnvVariables

from kafka import KafkaConsumer


def main():
    print("Starting consumer")
    try:
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            api_version=(0, 10, 1)
        )
        for message in consumer:
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key, message.value))

    except Exception as e:
        print(e)
        print(f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}, {EnvVariables.KAFKA_TOPIC_NAME.get_env()}')
        logging.info('Connection successful', e)
