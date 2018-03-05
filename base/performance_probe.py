# -*- coding: utf-8 -*-
import tornado.gen
import tornado.httpclient
import json
import time
import psutil

from loggers import SystemLogger
sys_logger=SystemLogger.instance().logger

@tornado.gen.coroutine
def get_url():
    
    sys_logger.info('begin')
    url = 'https://www.heiniubao.com/fulishe'
    response = yield tornado.httpclient.AsyncHTTPClient().fetch(url)
    sys_logger.info(psutil.net_io_counters())
    if response:
#         print response.body
        sys_logger.info('end')
        
if __name__ == "__main__": 
    while True:
        time.sleep(1)
        tornado.ioloop.IOLoop.current().run_sync(lambda: get_url())
