from typing import Union
from fastapi import Query


class Paginator:
    def __init__(
        self,
        page_size: Union[int, None] = Query(default=50, alias='page[size]'),
        page_number: Union[int, None] = Query(default=1, alias='page[number]')
    ):
        self.page_size = page_size
        self.page_number = (page_number - 1) * page_size
