from rq import Queue as RQueue  # type: ignore
from os import getenv
import redis

redis_host = getenv('REDIS_HOST')

if not redis_host:
    raise Exception('Redis host is invalid')

redis_scheduler = RQueue(connection=redis.from_url(redis_host))
