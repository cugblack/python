#!/usr/bin/env python
import redis, time

pool = redis.ConnectionPool(host = 'localhost',port = 6379, decode_responses = True)

r = redis.Redis(connection_pool = pool)
#r.set('name','cugblack', ex = 3)
#print r.get('name')
#time.sleep(3)
#print r.get('name')

r.hset('hash1', 'k1', 'v1')
r.hset('hash2', 'k2', 'v2')

print r.hkeys('hash1')
print r.hget('hash2', 'k2')
print r.hmget('hash1', 'k1', 'k2')
