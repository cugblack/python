#!/usr/bin/env python
import redis, time
import config

pool = redis.ConnectionPool(host = config.HOST, port = config.PORT, decode_responses = True)

r = redis.Redis(connection_pool = config.CONNECTION_POOL)
#r.set('name','cugblack', ex = 3)
#print r.get('name')
#time.sleep(3)
#print r.get('name')

r.hset('hash1', 'k1', 'v1')
r.hset('hash2', 'k2', 'v2')

print r.hkeys('hash1')
print r.hget('hash2', 'k2')
print r.hmget('hash1', 'k1', 'k2')
