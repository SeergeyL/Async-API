from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.response_description import PERSON_NOT_FOUND
from api.paginator import Paginator
from api.v1.response_models import Person, PersonDetail, PersonFilm
from services.persons import get_person_service, PersonService

router = APIRouter()


@router.get('/search', response_model=List[PersonDetail])
async def person_search(query: Optional[str] = Query(default=None),
                        paginator: Paginator = Depends(Paginator),
                        person_service: PersonService = Depends(get_person_service)) -> List[PersonDetail]:
    persons = await person_service.search_person(query, paginator.page_size, paginator.page_number)
    return [PersonDetail(id=person.id, full_name=person.name, roles=person.roles) for person in persons]


@router.get('/{person_id}',
            response_model=Person,
            summary='Информация по участнику',
            description='Детальная информация участника кинопроизведения',
            response_description='Фамилия Имя',)
async def person_details(person_id: str,
                         person_service=Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return Person(id=person.id, name=person.name)


@router.get('/{person_id}/film', response_model=List[PersonFilm])
async def person_films(
        person_id: str, person_service: PersonService = Depends(get_person_service)) -> List[PersonFilm]:
    films = await person_service.get_person_films(person_id)
    if films is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return [PersonFilm(id=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get('/',
            response_model=List[Person],
            summary='Список участников',
            description='Список всех участников кинопроизведений',
            response_description='Фамилия Имя',)
async def persons_listing(
                paginator: Paginator = Depends(Paginator),
                filters: List[str] = Query(default=[]),
                sort_field: str = Query(default=None),
                person_service = Depends(get_person_service),
            ) -> List[Person]:
    persons = await person_service.get_persons(
                        page_num=paginator.page_number,
                        page_size=paginator.page_size,
                        filters=filters,
                        sort_field=sort_field,
                    )
    persons = [Person(id=person.id, name=person.name)
                                                 for person in persons]
    return persons
