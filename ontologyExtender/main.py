from json import dumps, loads

from kafka import KafkaConsumer, KafkaProducer
import threading

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda x: dumps(x).encode('utf-8'),
                         api_version=(0, 10, 1)
                         )

consumer = KafkaConsumer(
    'ontologies',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    # group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    api_version=(0, 10, 1)
)


def register_kafka_listener(topic, listener):
    # Poll kafka
    def poll():
        print("About to start polling for topic:", topic)
        consumer.poll(timeout_ms=6000)
        print("Started Polling for topic:", topic)
        for msg in consumer:
            print("Entered the loop\nKey: ", msg.key, " Value:", msg.value)
            kafka_listener(msg)

    print("About to register listener to topic:", topic)
    t1 = threading.Thread(target=poll)
    t1.start()
    print("started a background thread")


def kafka_listener(data):
    print("Image Ratings:\n", data.value.decode("utf-8"))
    # return to kafka
    producer.send('ontologies', data.value + b' processed')


register_kafka_listener('ontologies', kafka_listener)
