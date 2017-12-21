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
        
        self.redis = {
            'host'      : '',
            'port'      : 0,
            'db'        : 0,
            'password'  : '',
            'expire'    : 0,
        }
        self.mysql = {
            'host'      : '',
            'db'        : '',
            'user'      : '',
            'password'  : '',
            }
        self.db_cluster_dict={} #{dbname:{host:db,user,pwd,}}
        
        self.db_cluster=[]
        
        dir = os.path.dirname(os.path.realpath(__file__))
        config_instance = ConfigParser.ConfigParser()
        config_instance.read(dir+'/config.ini')
        
        for key in self.redis:
            if type(self.redis[key]) == int:
                self.redis[key] = int(config_instance.get('redis', key))
            else:
                self.redis[key] = config_instance.get('redis', key)
                
        self.db_cluster = config_instance.get('db_cluster', 'db').split(',')
        
        for db in self.db_cluster:
            db_name = db.split(':')[0]
            for key in self.mysql:
                each_dict={}
                each_dict[key] = config_instance.get(db_name, key)
                self.db_cluster_dict[db_name] = each_dict