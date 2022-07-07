from http import HTTPStatus
from typing import Optional

from api.check_auth import auth_required
from api.paginator import Paginator
from api.response_description import FILM_NOT_FOUND
from api.v1.response_models import Film, FilmDetails
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from services.films import FilmService, get_film_service

router = APIRouter()


@router.get('/',
            response_model=list[Film],
            summary='Список кинопроизведений',
            description='Список всех кинопроизведений',
            response_description='Название и рейтинг фильма',)
async def films(
    paginator: Paginator = Depends(Paginator),
    genre_filter: list[str] = Query(default=[], alias='filter[genre]'),
    sort: str = Query(default='-imdb_rating'),
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_films(
        page_size=paginator.page_size,
        page_number=paginator.page_number,
        genre_filter=genre_filter,
        sorting=sort
    )

    return [Film.parse_obj(film) for film in films]


@router.get('/search',
            response_model=list[Film],
            summary='Поиск кинопроизведений',
            description='Полнотекстовый поиск по кинопроизведениям',
            response_description='Название и рейтинг фильма',)
async def film_search(
    query: str,
    paginator: Paginator = Depends(Paginator),
    sort: str = Query(default='-imdb_rating'),
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.search_films(
        query=query,
        page_size=paginator.page_size,
        page_number=paginator.page_number,
        sorting=sort
    )

    return [Film.parse_obj(film) for film in films]


@router.get('/{film_id}',
            summary='Детали кинопроизведения',
            description='Детальная информация по кинопроизведению',
            response_description='Название, рейтинг, описание, жанры и участники фильма',)
@auth_required
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
    authorization: Optional[str] = Header(default=None)
) -> FilmDetails:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return FilmDetails.parse_obj(film)
