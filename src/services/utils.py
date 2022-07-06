from functools import wraps
from typing import Any

import orjson
from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from db.cache import get_cache

def default(obj):
    if isinstance(obj, BaseModel):
        return pydantic_encoder(obj)


def make_key(key: str, kwargs: Any):
    result = [key]
    for item in sorted(kwargs.items()):
        result.extend(item)
    result = map(str, result)
    return '::'.join(result)


def cache(key, expires: int = 60):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            nonlocal key

            cache = await get_cache()

            key_ = make_key(key, kwargs)

            result = await cache.conn.get(key_)
            if result:
                return orjson.loads(result)

            result = await func(*args, **kwargs)
            serialized = orjson.dumps(result, default=default).decode()
            await cache.conn.set(key_, serialized, expire=expires)
            return result
        return inner
    return func_wrapper
