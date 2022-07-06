import logging

from redis import Redis
from tests.settings import get_test_settings

from backoff import backoff

log = logging.getLogger(__name__)

test_settings = get_test_settings()

log.info("Waiting for Redis...")

@backoff()
def wait_for_redis():
    redis_client = Redis(test_settings.redis_host)
    redis_client.ping()


wait_for_redis()
log.info("Redis started")
