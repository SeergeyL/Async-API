import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch


@pytest.fixture(scope='session')
async def es_client(test_settings):
    client = AsyncElasticsearch(hosts=[test_settings.es_host], verify_certs=True)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client(test_settings):
    client = await aioredis.create_redis_pool(
                    (test_settings.redis_host, test_settings.redis_port),
                    minsize=10,
                    maxsize=20
                )
    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='function')
async def redis_session(redis_client):
    await redis_client.flushall()
