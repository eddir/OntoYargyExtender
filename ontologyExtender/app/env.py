import os
from enum import Enum


class EnvironmentVariables(str, Enum):
    KAFKA_TOPIC = 'KAFKA_TOPIC'
    KAFKA_SERVER = 'KAFKA_SERVER'
    KAFKA_PORT = 'KAFKA_PORT'
    PG_USER = 'PG_USER'
    PG_PASSWORD = 'PG_PASSWORD'
    PG_HOST = 'PG_HOST'
    PG_PORT = 'PG_PORT'
    PG_DATABASE = 'PG_DATABASE'
    PUSHER_APP_ID = 'PUSHER_APP_ID'
    PUSHER_APP_KEY = 'PUSHER_APP_KEY'
    PUSHER_APP_SECRET = 'PUSHER_APP_SECRET'
    PUSHER_CLUSTER = 'PUSHER_CLUSTER'

    def get_env(self, variable=None):
        return os.environ.get(self, variable)
