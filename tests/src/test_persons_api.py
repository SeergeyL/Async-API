from http import HTTPStatus
import pytest
from tests.testdata import common
from tests.testdata.es_data import persons_data, movies_data


@pytest.mark.asyncio
async def test_persons_index_page(prepare_data, redis_session, make_get_request):
    response = await make_get_request('persons')
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(persons_data)


@pytest.mark.asyncio
async def test_persons_details(redis_session, make_get_request):
    person = common.get_random_record_from_testdata(persons_data)
    response = await make_get_request(f'persons/{person["id"]}')

    assert response.status == HTTPStatus.OK
    assert isinstance(response.body, dict) == True

    assert person['name'] == response.body['name']
    assert person['id'] == response.body['id']


@pytest.mark.asyncio
async def test_persons_films(redis_session, make_get_request):
    person = common.get_random_record_from_testdata(persons_data)
    response = await make_get_request(f'persons/{person["id"]}/film')

    cnt = 0
    for movie in movies_data:
        actors = [actor['id'] for actor in movie['actors']]
        if person['id'] in actors:
            cnt += 1

    assert response.status == HTTPStatus.OK
    assert len(response.body) == cnt
