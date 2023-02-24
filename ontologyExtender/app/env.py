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

    def get_env(self, variable=None):
        return os.environ.get(self, variable)
