from http import HTTPStatus
import pytest
import logging

from tests.testdata.es_data import movies_data
from tests.testdata.common import get_random_record_from_testdata

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_one_film(prepare_data, make_get_request, redis_session):

    # Посылаем запрос в сервис.
    logger.debug("Sending request for the one exising film ...")
    expected = get_random_record_from_testdata(movies_data)
    response = await make_get_request(
                        method=f'films/{expected["id"]}')
    logger.debug("Response:")
    logger.debug(response.body)

    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert response.body['title'] == expected['title']


@pytest.mark.asyncio
async def test_not_ex_film(make_get_request, redis_session):
    # Посылаем запрос в сервис.
    logger.debug("Sending request for the non-exising film ...")
    response = await make_get_request(
                        method='films/axxxxxx-a9c3-4a26-94db-9cf85ad8f3ec')
    logger.debug("Response:")
    logger.debug(response.body)
    expected = {
        "detail": "film not found"
    }
    # Проверка результата
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body == expected


@pytest.mark.asyncio
async def test_list_films(make_get_request, redis_session):
    # Посылаем запрос в сервис.
    logger.debug("Sending request for the list of films ...")
    response = await make_get_request(
                        method='films',
                        )
    logger.debug("Response:")
    logger.debug(response.body)
    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(movies_data)
