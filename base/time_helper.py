'''
@author: abc
'''
from datetime import datetime,date,time,timedelta
import time 
from calendar import timegm
from scheduler.util import datetime_to_utc_timestamp,convert_to_datetime
from pytz import timezone, utc
from tzlocal import get_localzone
import re

import threading
# t=time.time()
# # print t
# print time.gmtime(t)
# print time.localtime(t)
# print datetime.fromtimestamp(t)
# print datetime.now()
# print datetime.utcnow()
# print datetime.now().utctimetuple()
# print datetime.now().timetuple()
# print timegm(datetime.now().utctimetuple())
# print datetime.now().timetuple()
# print timegm(datetime.now().timetuple())
# print datetime.now().microsecond/1000000

d1=datetime.now()
d2=convert_to_datetime(datetime.now(),utc,'test')
d3=convert_to_datetime(datetime.now(),get_localzone(),'test')
t1=datetime_to_utc_timestamp(d1)
t2=datetime_to_utc_timestamp(d2)
t3=datetime_to_utc_timestamp(d3)
print d1
print d2
print d3
print t1
print t2
print t3

# map=dict(name='wxf')
# print map
# _ = 'test'
# file = '{}_error.log'.format(_) if _ is not None else 'default'
# print file
 
# a=time.time()
# for i in range(500):
#     print i
# b=time.time()
# 
# print int(b-a)
# print datetime.now()
# print date.today()
# print time()
# print (str(),str()

# start=datetime.combine(date.today()+timedelta(days=-1), time())
# end=datetime.combine(date.today(), time())
# print start,end



class CoreCache(object):
    _instance_lock = threading.Lock()

    @staticmethod
    def instance():
        if not hasattr(CoreCache, "_instance"):
            with CoreCache._instance_lock:
                if not hasattr(CoreCache, "_instance"):
                    CoreCache._instance = CoreCache()
        return CoreCache._instance

    def __init__(self):
        self.cache_storage={}

    def get_next_date(self):

        key = datetime.datetime.now().strftime("%Y-%m-%d")
        if self.cache_storage.get(key, ''):
            print 'get from cache'
            return self.cache_storage.get(key)
        else:
            day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            day = time.strptime(day, "%Y-%m-%d")
            day = int(time.mktime(day))
            self.cache_storage[key]=(day + 86400)
            print 'get from caculator'
            return (day + 86400)

# print CoreCache.instance().get_next_date()
# print CoreCache.instance().get_next_date()
# print CoreCache.instance().get_next_date()
# print CoreCache.instance().get_next_date()
