import logging
import os
import sys
from json import loads, dumps
from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from psycopg2 import Error

from app.enum import EnvironmentVariables as EnvVariables


def main():
    print("Starting consumer")

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

            for message in consumer:
                if message.value['action'] == 'parse':
                    print("parsing")

                elif message.value['action'] == 'fill':
                    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                         message.offset, message.key, message.value))
                    task_id = message.value['id']
                    # load ontology.owl and facts.xml from database into local files then run the fill task
                    cursor.execute("SELECT owl, facts, status FROM panel_filledontology WHERE id = %s", (task_id,))
                    record = cursor.fetchone()

                    # check whether the ontology is already filled
                    if record is not None and record[2] == "pending":
                        try:
                            print("writing owl file with a length of", len(record[0]))
                            with open('ontology.owl', 'w') as f:
                                f.write(record[0])
                            print("writing facts file with a length of", len(record[1]))
                            with open('facts.xml', 'w') as f:
                                f.write(record[1])

                            os.system('chmod +x ./bin/OntologyExtender')
                            os.system('./bin/OntologyExtender')

                            # save into result field in database
                            with open('result.owl', 'r') as f:
                                result = f.read()
                                print("Writing result with a length of", len(result))
                                cursor.execute("UPDATE panel_filledontology SET result = %s WHERE id = %s", (result, task_id))
                                connection.commit()

                                producer.send(kafka_topic, {
                                    'id': task_id,
                                    'action': 'done',
                                })

                                cursor.execute("UPDATE panel_filledontology SET status = %s WHERE id = %s", ("done", task_id))
                                connection.commit()
                                print("Record updated successfully ")

                            print("Ontology Filler finished")
                        except (Exception, Error) as error:
                            print("Error while connecting to PostgreSQL: ", error, " - in line ", sys.exc_info()[-1].tb_lineno)
                            # update state to failed
                            cursor.execute("UPDATE panel_filledontology SET status = %s WHERE id = %s", ("failed", task_id))
                            connection.commit()

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
