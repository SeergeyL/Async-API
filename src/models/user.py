from typing import Optional

from .utils import OrjsonModel


class Role(OrjsonModel):
    name: str
    description: Optional[str]


class User(OrjsonModel):
    email: str
    roles: list[Role]
