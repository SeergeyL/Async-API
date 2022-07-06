import json
from functools import lru_cache
from typing import Dict, Optional, List, Union
from uuid import UUID

from elasticsearch import NotFoundError
from fastapi import Depends
from pydantic import parse_obj_as

from db.storage import get_storage, AbstractStorage
from db.cache import get_cache, AbstractCache
from models.film import FilmMinified
from models.person import Person, PersonDetail
from services.es_queries import person_find, person_roles_find
from services.utils import cache

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService:
    def __init__(self, cache: AbstractCache, storage: AbstractStorage):
        self.cache = cache
        self.storage = storage

    async def get_by_id(self, person_id: str) -> Optional[PersonDetail]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    # @cache('persons', expires=PERSON_CACHE_EXPIRE_IN_SECONDS)
    async def get_persons(self,
                        page_size: int,
                        page_num: int,
                        filters: List[str],
                        sort_field: Union[str, None]  = None
                        ) -> Optional[List[Person]]:

        req_body = {
            "size": page_size,
            "from": page_num,
            "query":{
                "match_all" : {}
            },
        }
        if sort_field and sort_field.lstrip('-') == "name":
            req_body["sort"] = [
                { "name.raw" : {"order" : "desc" if sort_field.startswith('-')
                                     else "asc"}}
            ]

        try:
            persons = await self.storage.search(
                                        index='persons',
                                        body=req_body,
                                    )
        except NotFoundError:
            return None
        return [Person(**person['_source']) for person in persons['hits']['hits']]
        
    async def _get_person_from_elastic(self, person_id: str) -> Optional[PersonDetail]:
        try:
            doc = await self.storage.get('persons', person_id)
        except NotFoundError:
            return None

        person_name = doc['_source']['name']
        person_roles = await self.get_person_roles(person_name)
        return PersonDetail(**doc['_source'], roles=person_roles)

    async def _person_from_cache(self, person_id: str) -> Optional[PersonDetail]:
        data = await self.cache.get(person_id)
        if not data:
            return None
        film = PersonDetail.parse_raw(data)
        return film

    async def _put_person_to_cache(self, person: Union[Person, PersonDetail]):
        await self.cache.set(str(person.id), person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def get_person_roles(self, person_name: str) -> List[Dict[str, List[Optional[str]]]]:
        roles = list()
        for role, query in person_roles_find.items():
            role_films = {'role': role, 'film_ids': list()}
            results = await self.storage.search(index='movies', body=query % person_name, size=100)
            for entry in results['hits']['hits']:
                role_films['film_ids'].append(entry['_source']['id'])
            roles.append(role_films)
        return roles

    async def search_person(self, search_name: str, page_size: int, page_num: int) -> List[PersonDetail]:
        key = f'persons-person_name-{search_name}-page_size-{page_size}-page_num-{page_num}'
        persons = await self._get_search_result_from_cache(key)
        if not persons:
            persons = await self._get_search_result_from_elastic(search_name, page_size, page_num)
            if not persons:
                return []
            await self._put_search_result_to_cache(key, persons)
            persons = [PersonDetail.parse_raw(entry) for entry in persons]

        return persons

    async def _get_search_result_from_cache(self, key: str) -> Optional[List[PersonDetail]]:
        data = await self.cache.get(key)
        if not data:
            return None
        persons = [PersonDetail.parse_raw(entry) for entry in json.loads(data)]
        return persons

    async def _put_search_result_to_cache(self, key: str, persons: List[Optional[str]]) -> None:
        await self.cache.set(key, json.dumps(persons), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _get_search_result_from_elastic(
            self, search_name: str, page_size: int = 20, page_num: int = 0) -> List[Optional[str]]:
        persons = list()
        results = await self.storage.search(index='persons', body=person_find % (search_name, page_size, page_num))
        for entry in results['hits']['hits']:
            person = await self.get_by_id(entry['_source']['id'])
            persons.append(person.json())
        return persons

    async def get_person_films(self, person_id: str) -> Optional[List[FilmMinified]]:
        person = await self.get_by_id(person_id)
        if not person:
            return None
        key = f'persons-person_name-{person.name}'

        films = await self._get_person_films_from_cache(key)
        if not films:
            films = await self._get_person_films_from_elastic(person.name)
            if not films:
                return []
            await self._put_person_films_to_cache(key, films)
            films = parse_obj_as(List[FilmMinified], films)
        return films

    async def _get_person_films_from_cache(self, key: str) -> Optional[List[FilmMinified]]:
        data = await self.cache.get(key)
        if not data:
            return None

        films = parse_obj_as(List[FilmMinified], json.loads(data))
        return films

    async def _put_person_films_to_cache(self, key: str, films: List[Dict[str, Union[str, UUID]]]) -> None:
        await self.cache.set(key, json.dumps(films), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _get_person_films_from_elastic(
            self, person_name: str) -> List[Optional[Dict[str, Union[str, UUID]]]]:
        films = list()
        for query in person_roles_find.values():
            results = await self.storage.search(index='movies', body=query % person_name, size=100)
            for entry in results['hits']['hits']:
                films.append(entry['_source'])
        return films


@lru_cache()
def get_person_service(
        cache: AbstractCache = Depends(get_cache),
        storage: AbstractStorage = Depends(get_storage),
) -> PersonService:
    return PersonService(cache, storage)
