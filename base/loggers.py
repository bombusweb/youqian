#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging.handlers
import threading
import time

class SystemLogger(object):
    _instance_lock = threading.Lock()
    
    @staticmethod
    def instance():
        if not hasattr(SystemLogger, "_instance"):
            with SystemLogger._instance_lock:
                if not hasattr(SystemLogger, "_instance"):
                    SystemLogger._instance = SystemLogger()
        return SystemLogger._instance
    
    def __init__(self):
        self.logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        path=os.path.dirname(os.path.realpath(__file__))
#         system_log_file=path+'/'+str(os.getpid())+'.sysem.log'
        system_log_file=path+'/'+'sysem.log'
        file_handler = logging.handlers.TimedRotatingFileHandler(
                            filename=os.path.join(path,system_log_file),
                            when='h',
                            interval=12,
                            backupCount=100
                        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel('DEBUG')
        
        
SystemLogger = SystemLogger.instance().logger

if __name__ == "__main__":  
#     SystemLogger=SystemLogger.instance().logger
#     while True:
#         time.sleep(30)
#         SystemLogger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    pass