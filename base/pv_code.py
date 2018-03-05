# -*- code: utf-8 -*-

import redis

redis_conn=dict(host='172.26.36.94',port=6379,db=1,password='heiniu!slave')

r=redis.StrictRedis(**redis_conn)





