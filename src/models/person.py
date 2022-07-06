'''
Модуль содержит модель для сущности Персона - Person.
Используется только в рамках бизнес-логики
'''
from typing import Dict, List, Union
from uuid import UUID

from .utils import OrjsonModel


class Person(OrjsonModel):
    id: UUID
    name: str


class PersonDetail(OrjsonModel):
    id: UUID
    name: str
    roles: List[Dict[str, Union[List[UUID], str]]]
