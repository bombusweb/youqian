# -*- coding: utf-8 -*-
'''
@author: abc
'''

from scheduler.jobstore import RedisJobStore
from scheduler.job import Job
from datetime import datetime, timedelta
redis=RedisJobStore(db=0,host='47.94.206.52',port=6379,password='wxf1983')
next_run_time= datetime.now() + timedelta(seconds=30)
# print next_run_time
obj={'name':'wxf','age':20,'address':'beijing','com':'blank cow','role':'develepor','next_run_time':next_run_time}

job=Job(**obj)
print ''
# redis.add_job(job)
# # 
# 
jobs = redis.get_due_jobs(datetime.now())
#  
for job in jobs:
    _= redis.lookup_job(job.id)
    print _
#     redis.remove_job(job.id)
