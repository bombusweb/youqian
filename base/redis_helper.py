# -*- coding: utf-8 -*-

import threading
import sys_config
import redis

class RedisMaster(object):
    _instance_lock = threading.Lock()
    @staticmethod
    def instance():
        if not hasattr(RedisMaster, "_instance"):
            with RedisMaster._instance_lock:
                if not hasattr(RedisMaster, "_instance"):
                    RedisMaster._instance = RedisMaster()
        return RedisMaster._instance
    def __init__(self):
        redis_conn = sys_config.SystemConfig.instance().redis_master
        self.redis_master=redis.StrictRedis(**redis_conn)
        
class RedisSlave(object):
    _instance_lock = threading.Lock()
    @staticmethod
    def instance():
        if not hasattr(RedisSlave, "_instance"):
            with RedisSlave._instance_lock:
                if not hasattr(RedisSlave, "_instance"):
                    RedisSlave._instance = RedisSlave()
        return RedisSlave._instance
    def __init__(self):
        redis_conn = sys_config.SystemConfig.instance().redis_slave
        self.redis_slave=redis.StrictRedis(**redis_conn)
        
if __name__ == "__main__":  
    print RedisMaster.instance().redis_master.set('com','heniubao')
    print RedisSlave.instance().redis_slave
