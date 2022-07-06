from functools import lru_cache
from typing import Optional

from elasticsearch import NotFoundError
from fastapi import Depends

from db.storage import get_storage, AbstractStorage
from db.cache import get_cache, AbstractCache
from models.film import Film
from services.utils import cache

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, cache: AbstractCache, storage: AbstractStorage):
        self.cache = cache
        self.storage = storage

    def _get_pagination_params(self, *, page_number: int, page_size: int) -> dict:
        return {
            'from': page_number,
            'size': page_size
        }

    def _get_genre_filter_params(self, genres: list[str]) -> dict:
        return {
            'query': {
                'nested': {
                    'path': 'genres',
                    'query': {
                        'bool': {
                            'should': [
                                {'match': {'genres.id': genre}}
                                for genre in genres
                            ]
                        }
                    }
                }
            },
        }

    def _get_sorting_params(self, sorting: list[str]) -> dict:
        return {
            'sort': [
                {'imdb_rating': 'desc' if sorting.startswith('-') else 'asc'}
            ],
        }

    def _get_search_params(self, query: str, fields: list[str]) -> dict:
        return {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": fields
                }
            }
        }

    @cache('movies', expires=FILM_CACHE_EXPIRE_IN_SECONDS)
    async def get_films(
        self,
        *,
        page_size: int,
        page_number: int,
        genre_filter: list[str],
        sorting: str
    ) -> list[Film]:
        params = {
            **self._get_sorting_params(sorting),
            **self._get_genre_filter_params(genre_filter),
            **self._get_pagination_params(page_number=page_number, page_size=page_size)
        }
        films = await self.storage.search(body=params)
        return [Film(**film['_source']) for film in films['hits']['hits']]

    @cache('movies', expires=FILM_CACHE_EXPIRE_IN_SECONDS)
    async def search_films(
        self,
        *,
        page_size: int,
        page_number: int,
        sorting: str,
        query: str
    ) -> list[Film]:
        params = {
            **self._get_pagination_params(page_size=page_size, page_number=page_number),
            **self._get_sorting_params(sorting),
            **self._get_search_params(query, ["title", "description"])
        }
        films = await self.storage.search(body=params)
        return [Film(**film['_source']) for film in films['hits']['hits']]

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.storage.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.cache.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.cache.set(str(film.id), film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        cache: AbstractCache = Depends(get_cache),
        storage: AbstractStorage = Depends(get_storage),
) -> FilmService:
    return FilmService(cache, storage)
