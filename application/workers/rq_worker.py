from os import getenv

import redis
from application import connect
from rq import Connection, Queue, Worker  # type: ignore

listen = ['high', 'default', 'low']

if __name__ == '__main__':
    redis_host = getenv('REDIS_HOST')

    if not redis_host:
        raise Exception('Redis host is invalid')

    conn = redis.from_url(redis_host)

    connect()

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=True)
