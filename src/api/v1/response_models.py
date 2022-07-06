from typing import Dict, List, Union
from uuid import UUID

from models.utils import OrjsonModel


class Person(OrjsonModel):
    id: UUID
    name: str


class PersonDetail(OrjsonModel):
    id: UUID
    full_name: str
    roles: List[Dict[str, Union[List[UUID], str]]]


class PersonFilm(OrjsonModel):
    id: UUID
    title: str
    imdb_rating: float


class Genre(OrjsonModel):
    id: UUID
    name: str


class Film(OrjsonModel):
    id: UUID
    title: str
    imdb_rating: float


class FilmDetails(OrjsonModel):
    id: UUID
    title: str
    imdb_rating: float
    description: str
    genres: list[Genre]
    actors: list[Person]
    writers: list[Person]
    director: list[str]
