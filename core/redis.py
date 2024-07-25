import redis
import aioredis


def get_redis_pool() -> redis.Redis:
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    return redis.Redis(connection_pool=pool)


def get_aio_redis_pool() -> aioredis.Redis:
    return aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
