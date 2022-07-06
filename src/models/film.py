'''
Модуль содержит модель для сущности Фильм - Film.
Используется только в рамках бизнес-логики
'''
from uuid import UUID
from typing import List, Optional
from .person import Person
from .genre import Genre

from .utils import OrjsonModel

class Film(OrjsonModel):
    id: UUID
    imdb_rating: float
    genres: List[Genre]
    title: str
    description: Optional[str]
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[Person]
    writers: List[Person]


class FilmMinified(OrjsonModel):
    id: str
    title: str
    imdb_rating: float
