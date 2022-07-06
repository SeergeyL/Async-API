import logging

from elasticsearch import Elasticsearch
from tests.settings import get_test_settings

from backoff import backoff

log = logging.getLogger(__name__)

test_settings = get_test_settings()

log.info("Waiting for Elasticsearch...")

@backoff()
def wait_for_es():
    es_client = Elasticsearch(hosts=test_settings.es_host)
    es_client.ping()

wait_for_es()
log.info("Elasticsearch started")
