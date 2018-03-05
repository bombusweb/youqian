# -*- coding: utf-8 -*-

from collections import  Mapping
from uuid import uuid4
from datetime import datetime, timedelta
import six
from tzlocal import get_localzone
from scheduler.util import (datetime_repr, repr_escape, convert_to_datetime)
from pytz import timezone, utc
from base.loggers import SystemLogger as logger

class Job(object):
    
    def __init__(self, id=None,**kwargs):  #key-value，存放job的内容
        super(Job, self).__init__()
        if(kwargs['kwargs'].has_key('next_run_time')):
            kwargs['next_run_time']=kwargs['kwargs'].pop('next_run_time')
#             kwargs['next_run_time']=kwargs['kwargs']['next_run_time']
        else:
            kwargs['next_run_time']= datetime.now() + timedelta(minutes=5)
#       kwargs['next_run_time']= datetime.now() + timedelta(minutes=5)

#         if next_run_time is not None:
#             kwargs['next_run_time']=next_run_time
#         else:
#             kwargs['next_run_time']= datetime.now() + timedelta(minutes=5)
            
        self._modify(id=id or uuid4().hex, **kwargs)
        logger.info('job id:%s, now:%s, next run time:%s' % (self.id,str(datetime.now()),str(kwargs['next_run_time'])))

    
    def _modify(self, **changes):
        
        approved = {}

        if 'id' in changes:
            value = changes.pop('id')
            if not isinstance(value, six.string_types):
                raise TypeError("id must be a nonempty string")
            if hasattr(self, 'id'):
                raise ValueError('The job ID may not be changed')
            approved['id'] = value

        if 'kwargs' in changes:
            kwargs = changes.pop('kwargs') if 'kwargs' in changes else self.kwargs
            if isinstance(kwargs, six.string_types) or not isinstance(kwargs, Mapping):
                raise TypeError('kwargs must be a dict-like object')
            approved['kwargs'] = kwargs

        if 'next_run_time' in changes:
            value = changes.pop('next_run_time')
            logger.info('未转化的时间：'+str(value))
            approved['next_run_time'] = convert_to_datetime(value, utc,'next_run_time')  
            logger.info('转化后的时间：'+str(approved['next_run_time']))      
            
        if changes:
            raise AttributeError('The following are not modifiable attributes of Job: %s' % ', '.join(changes))

        for key, value in six.iteritems(approved):
            setattr(self, key, value)

    def __getstate__(self):
        
        return {
            'id': self.id,
            'kwargs':self.kwargs,
            'next_run_time': self.next_run_time
        }

    def __setstate__(self, state):
        self.id = state['id']
        self.kwargs = state['kwargs']
        self.next_run_time = state['next_run_time']

    def __eq__(self, other):
        if isinstance(other, Job):
            return self.id == other.id
        return NotImplemented

    def __repr__(self):
        return '<Job (id=%s)>' % repr_escape(self.id)

    def __str__(self):
        return repr_escape(self.__unicode__())

    def __unicode__(self):
        if hasattr(self, 'next_run_time'):
            status = ('next run at: ' + datetime_repr(self.next_run_time) if
                      self.next_run_time else 'paused')
        else:
            status = 'pending'

        return u'job id: %s (kwargs: %s, %s)' % (self.id,self.kwargs, status)
