import logging
import os
import sys
from json import loads, dumps
from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from psycopg2 import Error

import pusher

from app.env import EnvironmentVariables as EnvVariables
from app.parser import get_xml, get_facts


def main():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=EnvVariables.PG_USER.get_env(),
                                      password=EnvVariables.PG_PASSWORD.get_env(),
                                      host=EnvVariables.PG_HOST.get_env(),
                                      port=EnvVariables.PG_PORT.get_env(),
                                      database=EnvVariables.PG_DATABASE.get_env())
        try:
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, " - PostgreSQL database")
            print("kafka topic: ", EnvVariables.KAFKA_TOPIC.get_env())

            kafka_topic = EnvVariables.KAFKA_TOPIC.get_env()

            # To consume latest messages and auto-commit offsets
            consumer = KafkaConsumer(
                kafka_topic,
                bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
                value_deserializer=lambda x: loads(x.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                api_version=(0, 10, 1)
            )
            producer = KafkaProducer(
                bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
                value_serializer=lambda x: dumps(x).encode('utf-8'),
                api_version=(0, 10, 1)
            )

            try:
                pusher_client = pusher.Pusher(
                    app_id=EnvVariables.PUSHER_APP_ID.get_env(),
                    key=EnvVariables.PUSHER_APP_KEY.get_env(),
                    secret=EnvVariables.PUSHER_APP_SECRET.get_env(),
                    cluster=EnvVariables.PUSHER_CLUSTER.get_env(),
                    ssl=True
                )

                for message in consumer:
                    if message.value['action'] == 'parse':
                        try:
                            task_id = message.value['id']
                            cursor.execute("SELECT text, owl, status, name FROM panel_filledontology WHERE id = %s", (task_id,))
                            record = cursor.fetchone()
                            if record is not None and record[2] == "pending":
                                facts = get_xml(get_facts(record[0]), record[3])
                                cursor.execute("UPDATE panel_filledontology SET facts = %s, status = 'filling' WHERE id = %s", (facts, task_id))
                                connection.commit()
                                producer.send(kafka_topic, {
                                    "id": message.value['id'],
                                    "action": "fill",
                                })
                        except Exception as e:
                            print("parsing error:", e)
                            producer.send(kafka_topic, {
                                "id": message.value['id'],
                                "action": "error",
                                "error": str(e)
                            })

                    elif message.value['action'] == 'fill':
                        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                             message.offset, message.key, message.value))
                        task_id = message.value['id']
                        # load ontology.owl and facts.xml from database into local files then run the fill task
                        cursor.execute("SELECT facts, owl, status, name FROM panel_filledontology WHERE id = %s", (task_id,))
                        record = cursor.fetchone()

                        # check whether the ontology is already filled
                        if record is not None and record[2] == "filling":
                            try:

                                with open('ontology.owl', 'w') as f:
                                    f.write(record[1])
                                with open('facts.xml', 'w') as f:
                                    f.write(record[0])

                                os.system('chmod +x ./bin/OntologyExtender')
                                os.system('./bin/OntologyExtender')

                                # save into result field in database
                                with open('result.owl', 'r') as f:
                                    result = f.read()
                                    cursor.execute("UPDATE panel_filledontology SET result = %s WHERE id = %s", (result, task_id))
                                    connection.commit()

                                    producer.send(kafka_topic, {
                                        'id': task_id,
                                        'action': 'done',
                                    })

                                    cursor.execute("UPDATE panel_filledontology SET status = %s WHERE id = %s", ("done", task_id))
                                    connection.commit()

                                    pusher_client.trigger('ontologies-tasks', 'fill-event', {
                                        'message': 'done',
                                        'ontology_id': task_id
                                    })

                            except (Exception, Error) as error:
                                print("Error while producing ontology filler task: ", error, " - in line ", sys.exc_info()[-1].tb_lineno)
                                # update state to failed
                                cursor.execute("UPDATE panel_filledontology SET status = %s WHERE id = %s", ("failed", task_id))
                                connection.commit()

            except Exception as e:
                print("Pusher error: ", e)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL: ", error, " - in line ", sys.exc_info()[-1].tb_lineno)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    except Exception as e:
        print(e)
        print(
            f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}, {EnvVariables.KAFKA_TOPIC_NAME.get_env()}')
        logging.info('Connection successful', e)
