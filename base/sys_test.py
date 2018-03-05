# -*- coding: utf-8 -*-

import base.coreutils


# receiver='wangxiaofei@heiniubao.com'
# title='测试'
# body='测试'
# 
# base.coreutils.send_email(receiver, title, body)


# from datetime import datetime,timedelta
# import re
# import time
# 
# DATE_REGEX = re.compile(
#     r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
#     r'(?: (?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})'
#     r'(?:\.(?P<microsecond>\d{1,6}))?)?')
# 
# 
# while True:
#     time.sleep(60)
#     mytime=datetime.now()-timedelta(minutes=5)
#     m = DATE_REGEX.match(str(mytime))
#     values = [(k, int(v or 0)) for k, v in m.groupdict().items() if k not in ('microsecond','second')]
#     values = dict(values)
#     datetime_ = datetime(**values)
#     lowerTime=datetime_-timedelta(minutes=5)
#     upperTime=datetime_
#     lowerTime=lowerTime.strftime('%Y-%m-%d %H:%M:%S')
#     upperTime=upperTime.strftime('%Y-%m-%d %H:%M:%S')
#     print lowerTime,upperTime


# a='中国'
# b=u'中国'
# aa={'country':a}
# bb={'country':b}
# print type(a),type(b)



# import datetime
# import json
# now = datetime.datetime.now()
# print json.dumps(now)





# dict={'naem':'wxf','address':'beijing'}
# print len(dict)


# 
# import datetime
# 
# 
# 
# time_prefix=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
# print time_prefix























# import datetime
# lower=datetime.datetime(2018,01,28)
# all_date_list=[]
#      
# for i in range(1,4):
#     lower=lower+datetime.timedelta(days = 1)
#     upper=lower+datetime.timedelta(days = 1)
#     lower_str=lower.strftime('%Y-%m-%d')
#     upper_str=upper.strftime('%Y-%m-%d')
#     print lower_str,upper_str



# import re
# QUESTION_REGEX = re.compile('^[Y|N]$')
# name='Y'
# print QUESTION_REGEX.match(name)





# class Person(object):
#     
#     def init(self):
#         print 'Person init'
#         
#     def say(self):
#         self.init()
#         print 'Person say'
#         
#         
# class Son(Person):
#     def init(self):
#         print 'Son init'
#         
# 
# 
#     
# 
# 
# son=Son()
# son.say()





# map={}
# map['name']='wxf'
# map['city']='beijing'
# map.pop('name')
# map.pop('city')
# map.pop('age','xxx')
# print map
# 
# if map:
#     print 'map is not empty'
# else:
#     print 'map is empty'
    
# list=[]
# list=None
# for date in list:
#     print date


# mobile='136*'
# 
# if mobile and not '*' in mobile:
#     print 'user input'
# else:
#     print 'system auto input'


# import  json
# custom={"信用卡": "有", "名下汽车": "无车", "月收入": "5千-1万", "名下房产": "无房", "寿险保单": "有", "期望贷款": "10000元", "您的职业": "公务员", "工作时间": "12个月内"}
# custom=json.dumps(custom)
# 
# custom = json.loads(custom)
# custom = {k.encode('utf-8'): v.encode('utf-8') for k, v in custom.items()}
# print custom

# print 22 in range(22, 56)


# import logging
# user_info_dict=None
# TEXT_MSG_TPL = """
# <xml>
# <ToUserName><![CDATA[%s]]></ToUserName>
# <FromUserName><![CDATA[%s]]></FromUserName>
# <CreateTime>%s</CreateTime>
# <MsgType><![CDATA[text]]></MsgType>
# <Content><![CDATA[%s]]></Content>
# <FuncFlag>0</FuncFlag>
# </xml>
# """
# TEXT_MSG_TPL=TEXT_MSG_TPL.replace('\n', '')
# print type(TEXT_MSG_TPL)
# logging.info(TEXT_MSG_TPL)
# print TEXT_MSG_TPL
# logging.debug('wxf')

# short_url='http://www'
# error_msg='error'
# result = short_url, error_msg
# print type(result)
dict={}
# dict['sex']=0
if dict.get('sex','')=='':
    print '0'