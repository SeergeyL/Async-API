""" В файле содержатся функции для подготовки данных для тестирования """
import random
from elasticsearch.helpers import async_bulk


def get_random_record_from_testdata(data):
    return random.choice(data)


async def upload_data(data, *, index, es_client):
    await async_bulk(es_client, data, index=index, refresh='wait_for')


def get_list_unique_values_by_key(data: list[dict], key):
    result = set()
    for record in data:
        values = [tuple(obj.items()) for obj in record[key]]
        result.update(values)
    return [dict(obj) for obj in result]
