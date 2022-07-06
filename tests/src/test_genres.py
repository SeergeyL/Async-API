from http import HTTPStatus
import pytest
import logging
from tests.testdata.common import get_random_record_from_testdata
from tests.testdata.es_data import genres_data

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_one_genre(prepare_data, make_get_request):

    # Посылаем запрос в сервис.
    logger.debug("Sending request for the one exising genre ...")
    expected = get_random_record_from_testdata(genres_data)
    response = await make_get_request(
                        method=f'genres/{expected["id"]}')
    logger.debug("Response:")
    logger.debug(response.body)

    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert response.body['name'] == expected['name']
    assert response.body['id'] == expected['id']


@pytest.mark.asyncio
async def test_not_ex_genre(redis_session, make_get_request):
    # Посылаем запрос в сервис.
    logger.debug("Sending request for the non-exising genre ...")
    response = await make_get_request(
                        method='genres/axxxxxx-a9c3-4a26-94db-9cf85ad8f3ec')
    logger.debug("Response:")
    logger.debug(response.body)
    expected = {
        "detail": "genre not found"
    }
    # Проверка результата
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body == expected


@pytest.mark.asyncio
async def test_list_genres(redis_session, make_get_request):
    # Посылаем запрос в сервис.
    logger.debug("Sending request for the list of genres ...")
    response = await make_get_request(
                        method='genres',
                        )
    logger.debug("Response:")
    logger.debug(response.body)
    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(genres_data)
