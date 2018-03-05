# -*- coding: utf-8 -*-

import redis
import cPickle
import datetime

def get_uv(hash_name,key):
    redis_conn=dict(host='172.26.36.94',port=6379,db=1,password='heiniu!slave')
    redis_instance=redis.StrictRedis(**redis_conn)
    user_list = []
    value = redis_instance.hget(hash_name, key)
    if value:
        user_list = cPickle.loads(value)
        return len(user_list)
    else:
        return 0
   
lower=datetime.datetime(2018,02,28)
for i in range(1,2):
    lower=lower+datetime.timedelta(days = 1)
    upper=lower+datetime.timedelta(days = 1)
    lower_str=lower.strftime('%Y-%m-%d')
    upper_str=upper.strftime('%Y-%m-%d')
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    print lower_str  
    loan_num=0
    financing_num=0
    home=0
    hash_name=lower_str+'_weixin_loan'
    loan_num=loan_num+get_uv(hash_name,'sudaizhijia')
    loan_num=loan_num+get_uv(hash_name,'rong360')
    loan_num=loan_num+get_uv(hash_name,'pinganpuhui')
    loan_num=loan_num+get_uv(hash_name,'heika')
    loan_num=loan_num+get_uv(hash_name,'huicheliandong')
    loan_num=loan_num+get_uv(hash_name,'dalujietiao')
    loan_num=loan_num+get_uv(hash_name,'niwodai')
    print '贷款推广导出:'+str(loan_num)
    financing_num=financing_num+get_uv(hash_name,'qianguanzi')
    financing_num=financing_num+get_uv(hash_name,'liminwang')
    print '理财推广导出:'+str(financing_num)
    home=home+get_uv(hash_name,'home')
    print '首页UV:'+str(home)
    app_uv=0
    app_uv+=get_uv(lower_str+'_weixin_auth_bind','auth-bind')
    print '总UV:'+str(app_uv)
    print '领券页UV:'+ str(get_uv(hash_name,'ticket'))
    print '贷款定制UV:'+ str(get_uv(hash_name,'evaluate-loan'))
    print '理财测评UV:'+ str(get_uv(hash_name,'evaluate-financing'))
    print '保费测算UV:'+ str(get_uv(hash_name,'evaluate-insu'))
    print '保险列表页UV:'+ str(get_uv(hash_name,'list-insu-ad'))
    print 'TKTravel:'+ str(get_uv(hash_name,'TKTravel'))
    print 'TKCancer:'+ str(get_uv(hash_name,'TKCancer'))