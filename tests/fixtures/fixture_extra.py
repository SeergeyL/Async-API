from dataclasses import dataclass
from typing import Optional

import pytest
from multidict import CIMultiDictProxy

from tests.testdata.common import upload_data
from tests.testdata.es_data import persons_data, movies_data, genres_data
from tests.testdata.indices import movies_schema, persons_schema, genres_schema
from tests.settings import get_test_settings, logger


@pytest.fixture(scope='session')
def test_settings():
    return get_test_settings()


@pytest.fixture(scope='session')
async def es_indexes(es_client, test_settings):
    index = test_settings.person_index
    if not await es_client.indices.exists(index):
        logger.info(f"Index {index} not found. Creating {index} ...")
        await es_client.indices.create(index=index, body=persons_schema)

    index = test_settings.movie_index
    if not await es_client.indices.exists(index):
        logger.info(f"Index {index} not found. Creating {index} ...")
        await es_client.indices.create(index, body=movies_schema)

    index = test_settings.genre_index
    if not await es_client.indices.exists(index):
        logger.info(f"Index {index} not found. Creating {index} ...")
        await es_client.indices.create(index, body=genres_schema)

    yield

    await es_client.indices.delete(index=test_settings.person_index)
    await es_client.indices.delete(index=test_settings.movie_index)
    await es_client.indices.delete(index=test_settings.genre_index)


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def prepare_data(es_indexes, test_settings, es_client):
    await upload_data(
        persons_data,
        index=test_settings.person_index,
        es_client=es_client
    )
    await upload_data(
        movies_data,
        index=test_settings.movie_index,
        es_client=es_client
    )
    await upload_data(
        genres_data,
        index=test_settings.genre_index,
        es_client=es_client
    )
    yield
    await es_client.delete_by_query(
        index=[
            test_settings.person_index,
            test_settings.movie_index,
            test_settings.genre_index
        ],
        body={'query': {'match_all': {}}}
    )


@pytest.fixture(scope="session")
def make_get_request(session, test_settings):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = 'http://{api_host}:{api_port}/api/{api_version}/{path}' \
            .format(**test_settings.dict(), path=method)
        logger.debug(f"URL: {url}")
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
