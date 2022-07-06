import logging
import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(__file__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-15s %(message)s')
cons_handler = logging.StreamHandler()
cons_handler.setFormatter(formatter)
root_logger.addHandler(cons_handler)
file_handler = logging.FileHandler("tests.log")
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

logger = root_logger


class TestSettings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    api_host: str = Field('127.0.0.1', env='API_HOST')
    api_port: str = Field('8000', env='API_PORT')
    api_version: str = Field('v1', env='API_VERSION')
    es_host: str = Field('http://elastic:123456@192.168.1.7:9200', env='ELASTIC_HOST')
    redis_host: str = Field('192.168.1.7', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')
    project_name: str = Field('movies', env='PROJECT_NAME')
    person_index: str = Field('persons', env='PERSON_INDEX')
    genre_index: str = Field('genres', env='GENRE_INDEX')
    movie_index: str = Field('movies', env='MOVIES_INDEX')


def get_test_settings() -> BaseSettings:
    logger.info("Loading test config settings from the environment...")
    return TestSettings()
