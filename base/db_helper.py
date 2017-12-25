#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys_config
import consistent
import torndb
import loggers

class MySQLHelper(object):
    _instance_lock = threading.Lock()
    
    @staticmethod
    def instance():
        if not hasattr(MySQLHelper, "_instance"):
            with MySQLHelper._instance_lock:
                if not hasattr(MySQLHelper, "_instance"):
                    MySQLHelper._instance = MySQLHelper()
        return MySQLHelper._instance
    
    
    def __init__(self):
        config = sys_config.SystemConfig.instance()
        db_nodes = {}
        for db in config.db_cluster:
            db_name = db.split(':')[0]
            db_weight = int(db.split(':')[1])
            db_nodes[db_name] = db_weight
        self.consistent= consistent.ConsistentHash(db_nodes)
        self.db_conn={}
        for db in config.db_cluster:
            db_name = db.split(':')[0]
            db_conn = torndb.Connection(
                        host = config.db_cluster_dict[db_name]['host'],
                        database = config.db_cluster_dict[db_name]['db'],
                        user = config.db_cluster_dict[db_name]['user'],
                        password = config.db_cluster_dict[db_name]['password'])
            self.db_conn[db_name]=db_conn
        
        
    def get_db_conn(self, id_no, phone):
        seed = phone + '_' + id_no
        db_name = self.consistent.get_node(seed)
        loggers.SystemLogger.info('id_no:%s, phone:%s, db name:%s' % (id_no, phone, db_name))
        return self.db_conn[db_name]
    def get_db_connect(self,id_no,phone):
        pass