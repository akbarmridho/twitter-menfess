from rq import Queue as RQueue  # type: ignore
from os import getenv
import redis


def get_redis_queue() -> RQueue:
    """Get redis queue

    Returns:
        RQueue: Redis queue instance
    """
    redis_host = getenv('REDIS_HOST')

    if not redis_host:
        raise Exception('Redis host is invalid')

    return RQueue(connection=redis.from_url(redis_host))
