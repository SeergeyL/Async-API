import abc
from typing import Optional
from aioredis import Redis


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    async def get(self):
        pass

    @abc.abstractmethod
    async def set(self):
        pass


class RedisCache(AbstractCache):
    def __init__(self, redis: Redis):
        self.conn = redis
    
    async def get(self, *args, **kwargs):
        return await self.conn.get(*args, **kwargs)

    async def set(self, *args, **kwargs):
        return self.conn.set(*args, **kwargs)


cache: Optional[AbstractCache] = None

# Функция понадобится при внедрении зависимостей
async def get_cache() -> AbstractCache:
    return cache
