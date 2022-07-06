import abc
from typing import Optional
from elasticsearch import AsyncElasticsearch


class AbstractStorage(abc.ABC):
    @abc.abstractmethod
    async def get(self):
        pass

    @abc.abstractmethod
    async def search(self):
        pass


class ElasticStorage(AbstractStorage):
    def __init__(self, es: AsyncElasticsearch):
        self.conn = es

    async def get(self, *args, **kwargs):
        return await self.conn.get(*args, **kwargs)

    async def search(self, *args, **kwargs):
        return await self.conn.search(*args, **kwargs)


storage: Optional[AbstractStorage] = None

# Функция понадобится при внедрении зависимостей
async def get_storage() -> AbstractStorage:
    return storage
