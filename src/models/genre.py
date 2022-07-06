'''
Модуль содержит модель для сущности Жанр - Genre.
Используется только в рамках бизнес-логики
'''
from uuid import UUID

from .utils import OrjsonModel

class Genre(OrjsonModel):
    id: UUID
    name: str
