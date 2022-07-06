from http import HTTPStatus

import pytest
from tests.testdata.common import get_random_record_from_testdata
from tests.testdata.es_data import movies_data, persons_data


@pytest.mark.asyncio
async def test_person_search(prepare_data, make_get_request):
    expected = get_random_record_from_testdata(persons_data)
    response = await make_get_request(
        method='persons/search',
        params={'query': expected['name']}
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1

    assert isinstance(response.body, list) is True

    assert response.body[0]['full_name'] == expected['name']
    assert response.body[0]['id'] == expected['id']


@pytest.mark.asyncio
async def test_movies_search(make_get_request):
    expected = get_random_record_from_testdata(movies_data)
    response = await make_get_request(
        method='films/search',
        params={
            'query': expected['title']
        }
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) > 0
