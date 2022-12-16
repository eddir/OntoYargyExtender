from kafka import KafkaConsumer, KafkaProducer
import threading

BOOTSTRAP_SERVERS = ['broker:9092']

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)


def register_kafka_listener(topic, listener):
    # Poll kafka
    def poll():
        # Initialize consumer Instance
        consumer = KafkaConsumer(topic, bootstrap_servers=BOOTSTRAP_SERVERS)

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
    producer.send('image_ratings', data.value + b' processed')


register_kafka_listener('topic1', kafka_listener)
