#!/usr/bin/env python
import redis, time
import config
from redis import RedisError


def redis_list():
    # CONNECTION_POOL = "pool"
    pool = redis.ConnectionPool(host=config.HOST, port=config.PORT, decode_responses=True)
    try:
        r = redis.Redis(connection_pool = pool)
        r.set('name','cugblack', ex = 3)
        print r.get('name')
        time.sleep(3)
        print r.get('name')
        print "success"
    except RedisError:
        print RedisError

if __name__ == "__main__":
    redis_list()