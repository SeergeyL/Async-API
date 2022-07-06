from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from api.response_description import GENRE_NOT_FOUND
from api.paginator import Paginator
from api.v1.response_models import Genre
from services.genres import get_genre_service

router = APIRouter()


@router.get('/{genre_id}',
            response_model=Genre,
            summary='Детали жанра',
            description='Детальная информация по жанру',
            response_description='Название жанра',)
async def genre_details(genre_id: str, 
                        genre_service=Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return Genre(id=genre.id, name=genre.name)


@router.get('/',
            response_model=List[Genre],
            summary='Список жанров',
            description='Список всех жанров',
            response_description='Название жанра',)
async def genres_listing(
                    paginator: Paginator = Depends(Paginator),
                    filters: List[str] = Query(default=[]),
                    sort_field: str = Query(default=None),
                    genre_service = Depends(get_genre_service)
                ) -> List[Genre]:
    genres = await genre_service.get_genres(
                        page_num=paginator.page_number,
                        page_size=paginator.page_size,
                        filters=filters,
                        sort_field=sort_field
                    )
    return genres
