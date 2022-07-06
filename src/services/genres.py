from functools import lru_cache
from typing import Optional, List, Union

from elasticsearch import NotFoundError
from fastapi import Depends

from db.storage import get_storage, AbstractStorage
from db.cache import get_cache, AbstractCache
from models.genre import Genre
from services.utils import cache

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService:
    def __init__(self, cache: AbstractCache, storage: AbstractStorage):
        self.cache = cache
        self.storage = storage

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    @cache('genres', expires=GENRE_CACHE_EXPIRE_IN_SECONDS)
    async def get_genres(self, 
                        page_size: int,
                        page_num: int,
                        filters: List[str],
                        sort_field: Union[str, None] = None
                        ) -> Optional[List[Genre]]:

        req_body = {
            'size': page_size,
            'from': page_num,
            'query':{
                "match_all" : {}
            }
        }
        if sort_field and sort_field.lstrip('-') == "name":
            req_body["sort"] = [
                { "name.raw" : {"order" : "desc" if sort_field.startswith('-')
                                     else "asc"}}
            ]
        try:
            genres = await self.storage.search(
                                            index='genres',
                                            body=req_body,
                                        )
        except NotFoundError:
            return None
        return [Genre(**genre['_source']) for genre in genres['hits']['hits']]

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.storage.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.cache.get(genre_id)
        if not data:
            return None

        film = Genre.parse_raw(data)
        return film

    async def _put_genre_to_cache(self, genre: Genre):
        await self.cache.set(str(genre.id), genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        cache: AbstractCache = Depends(get_cache),
        storage: AbstractStorage = Depends(get_storage),
) -> GenreService:
    return GenreService(cache, storage)
