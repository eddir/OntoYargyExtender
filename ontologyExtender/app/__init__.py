import logging
import os
import sys
import uuid
from json import loads, dumps
from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from psycopg2 import Error
import boto3

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

                try:

                    s3 = boto3.client(
                        aws_access_key_id=EnvVariables.AWS_ACCESS_KEY_ID.get_env(),
                        aws_secret_access_key=EnvVariables.AWS_SECRET_ACCESS_KEY.get_env(),
                        region_name=EnvVariables.AWS_REGION_NAME.get_env(),
                        service_name='s3',
                        endpoint_url=EnvVariables.AWS_S3_ENDPOINT_URL.get_env()
                    )

                    for message in consumer:
                        if message.value['action'] == 'parse':
                            try:
                                task_id = message.value['id']
                                cursor.execute(
                                    "SELECT text, owl, status, name FROM panel_filledontology WHERE id = %s",
                                    (task_id,)
                                )
                                record = cursor.fetchone()
                                if record is not None and record[2] == "pending":
                                    text_file = s3.get_object(
                                        Bucket=EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(),
                                        Key=record[0]
                                    )

                                    text_content = text_file['Body'].read().decode('utf-8')

                                    print(len(text_content))

                                    facts = get_xml(get_facts(text_content), record[3])

                                    # generate id for the owl file (random)
                                    facts_file = "/facts/" + str(uuid.uuid4()) + ".xml"
                                    s3.put_object(
                                        Bucket=EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(),
                                        Key=facts_file,
                                        Body=facts
                                    )
                                    cursor.execute(
                                        "UPDATE panel_filledontology SET facts = %s, status = 'filling' WHERE id = %s",
                                        (facts_file, task_id)
                                    )
                                    connection.commit()
                                    producer.send(kafka_topic, {
                                        "id": message.value['id'],
                                        "action": "fill",
                                    })
                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                print("parsing suka error at line ({0}): {1} ".format(exc_tb.tb_lineno, e))
                                producer.send(kafka_topic, {
                                    "id": message.value['id'],
                                    "action": "error",
                                    "error": str(e)
                                })

                        elif message.value['action'] == 'fill':
                            task_id = message.value['id']
                            # load ontology.owl and facts.xml from database into local files then run the fill task
                            cursor.execute("SELECT facts, owl, status, name FROM panel_filledontology WHERE id = %s",
                                           (task_id,))
                            record = cursor.fetchone()

                            # check whether the ontology is already filled
                            if record is not None and record[2] == "filling":
                                try:
                                    facts_path = record[0]
                                    owl_path = record[1]
                                    # save to ontology.owl and facts.xml\
                                    # idk why this part is not working
                                    # s3.download_file(EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(), facts_path, 'ontology.owl')
                                    # s3.download_file(EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(), owl_path, 'facts.xml')

                                    facts = s3.get_object(
                                        Bucket=EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(),
                                        Key=facts_path
                                    )
                                    owl = s3.get_object(
                                        Bucket=EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(),
                                        Key=owl_path
                                    )

                                    facts_content = facts['Body'].read().decode('utf-8')
                                    owl_content = owl['Body'].read().decode('utf-8')

                                    with open('ontology.owl', 'w') as f:
                                        f.write(owl_content)

                                    with open('facts.xml', 'w') as f:
                                        f.write(facts_content)

                                    os.system('chmod +x ./bin/OntologyExtender')
                                    os.system('./bin/OntologyExtender')

                                    result_file = "/owl_filled/" + str(uuid.uuid4()) + ".owl"
                                    s3.upload_file(
                                        'result.owl',
                                        EnvVariables.AWS_STORAGE_BUCKET_NAME.get_env(),
                                        result_file
                                    )
                                    cursor.execute("UPDATE panel_filledontology SET result = %s WHERE id = %s",
                                                   (result_file, task_id))
                                    connection.commit()

                                    producer.send(kafka_topic, {
                                        'id': task_id,
                                        'action': 'done',
                                    })

                                    cursor.execute("UPDATE panel_filledontology SET status = %s WHERE id = %s",
                                                   ("done", task_id))
                                    connection.commit()

                                    pusher_client.trigger('ontologies-tasks', 'fill-event', {
                                        'message': 'done',
                                        'ontology_id': task_id
                                    })

                                except (Exception, Error) as error:
                                    print("Error while producing ontology filler task: ", error, " - in line ",
                                          sys.exc_info()[-1].tb_lineno)
                                    # update state to failed
                                    cursor.execute("UPDATE panel_filledontology SET status = %s WHERE id = %s",
                                                   ("failed", task_id))
                                    connection.commit()

                except Exception as e:
                    print("S3 error: ", e)

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
