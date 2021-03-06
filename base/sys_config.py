#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import os
import ConfigParser
class SystemConfig(object):
    _instance_lock=threading.Lock()
    
    @staticmethod
    def instance():
        if not hasattr(SystemConfig, '_instance'):
            with SystemConfig._instance_lock:
                if not hasattr(SystemConfig, '_instance'):
                    SystemConfig._instance=SystemConfig()
        return SystemConfig._instance
    
    
    def __init__(self):
        
        self.redis_master = {
            'host'      : '',
            'port'      : 0,
            'db'        : 0,
            'password'  : ''
        }
        self.redis_slave = {
            'host'      : '',
            'port'      : 0,
            'db'        : 0,
            'password'  : ''
        }
        self.mysql = {
            'host'      : '',
            'db'        : '',
            'user'      : '',
            'password'  : ''
            }
        
        
        self.pycket = {
            'engine': '',
            'storage_host': '',
            'storage_port': '',
            'storage_password': '',
            'storage_db_sessions': '',
            'storage_db_notifications': '',
            'storage_max_connections': '',
            'cookies_expires_days': '',
            'cookies_expires': '',
            'domain':''
        }
        
        self.db_cluster_dict={} #{dbname:{host:db,user,pwd,}}
        
        self.db_cluster=[]
        
        dir = os.path.dirname(os.path.realpath(__file__))
        config_instance = ConfigParser.ConfigParser()
        config_instance.read(dir+'/config2.ini')
        
        for key in self.redis_master:
            if type(self.redis_master[key]) == int:
                self.redis_master[key] = int(config_instance.get('redis_master', key))
            else:
                self.redis_master[key] = config_instance.get('redis_master', key)
        
        for key in self.redis_slave:
            if type(self.redis_slave[key]) == int:
                self.redis_slave[key] = int(config_instance.get('redis_slave', key))
            else:
                self.redis_slave[key] = config_instance.get('redis_slave', key)
                        
        self.db_cluster = config_instance.get('db_cluster', 'db').split(',')
        
        for db in self.db_cluster:
            db_name = db.split(':')[0]
            each_dict={}
            for key in self.mysql:
                each_dict[key] = config_instance.get(db_name, key)
                self.db_cluster_dict[db_name] = each_dict
                
        for key in self.pycket:
            self.pycket[key] = config_instance.get('pycket', key)
