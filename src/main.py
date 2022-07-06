import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import storage, cache
from db.storage import ElasticStorage
from db.cache import RedisCache

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    # Инициализируем кэш
    redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    cache.cache = RedisCache(redis)

    # # Инициализируем хранилище
    elastic = AsyncElasticsearch(hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    storage.storage = ElasticStorage(elastic)


@app.on_event('shutdown')
async def shutdown():
    cache.conn.close()
    await cache.conn.wait_closed()
    await storage.conn.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['Кинопроизведения'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['Жанры'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['Участники'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
