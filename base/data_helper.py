# -*- coding: utf-8 -*-

import torndb
import sys_config
import json

import redis

import xlwt
import os

import cPickle

config = sys_config.SystemConfig.instance()
db_name='mydb_1'
db_conn = torndb.Connection(
                        host = config.db_cluster_dict[db_name]['host'],
                        database = config.db_cluster_dict[db_name]['db'],
                        user = config.db_cluster_dict[db_name]['user'],
                        password = config.db_cluster_dict[db_name]['password'])

def get_subchnnel(lower,upper):
    sql='select * from t_loan_records where create_time > \'%s\' and create_time < \'%s\' ' % (lower,upper)
    record_list = db_conn.query(sql)
    subchannel_set=set()
    for record in record_list:
        subchannel_set.add(record.subchannel)
    return subchannel_set
    
    
#dict = {'':{'large':,'small':}}
def get_records_by_subchannel_in_dict(lower,upper,subchannel):
    sql='select * from t_loan_records where create_time > \'%s\' and create_time < \'%s\' and subchannel = \'%s\' ' % (lower,upper,subchannel)
    dict_outer={}
    record_list = db_conn.query(sql)
    for record in record_list:
        loan_type=get_loan_type(record)
        dict_inner=dict_outer.get(record.phone,None)
        if dict_inner:
#             if loan_type not in dict_inner.keys():
#                 dict_inner[loan_type]=record
#                 dict_outer[record.phone]=dict_inner
#             else:
#                 _=dict_inner[loan_type]
#                 if _.policy_id:
#                     pass
#                 elif record.policy_id:
#                     dict_inner[loan_type]=record
#                     dict_outer[record.phone]=dict_inner
#                 else:
#                     pass
            pass
        else:
            dict_outer[record.phone]={loan_type:record}
        
    return dict_outer
  
def get_loan_type(loan_info):
    is_large_loan = int(float(loan_info.amount)) in range(5000, 500001) and int(loan_info.age) in range(28, 51) and loan_info.credit == 'Y'
    if is_large_loan:
        return 'large'
    else:
        return 'small'
    
    
def get_custom_type(record):
    custom=record.custom
    custom=json.loads(custom)
    if not custom.get(u'名下汽车') or custom.get(u'名下汽车') == u'无车':
            if_car = ''
    else:
            if_car = 'have'
    if not custom.get(u'名下房产') or custom.get(u'名下房产') == u'无房':
        if_house = ''
    else:
        if_house = 'have'
    if not custom.get(u'寿险保单') or custom.get(u'寿险保单') == u'没有':
        if_policy = ''
    else:
        if_policy = 'have'
        
    if (if_car and if_house and if_policy):
        return 3
    
    elif (if_car and if_house):
        return 2
    
    elif (if_house and if_policy):
        return 2
        
    elif (if_car and if_policy):
        return 2
    elif (if_car or if_house or if_policy):
        return 1
    else:
        return 0
    
def stats_by_subchannel_in_list(dict,lower,upper):
    submit_phone=0
    submit_captcha=0
    submit_record=0
    large_loan=0
    small_loan=0
    age_25=0
    age_25_credit=0
    age_25_credit_one=0
    age_25_credit_two=0
    age_25_credit_three=0
    zx_submit=0
    zx_success=0
    zx_effective=0
    loan_fdb=0
    loan_bx=0
    loan_zy=0
    
    for key,value in dict.items():
        mobile=key
        dict_inner=value
        submit_record+=len(value)
        if dict_inner.get('large',''):
            large_loan+=1
            large_apply=dict_inner.get('large','')
            if large_apply.age in range(20,51):
                age_25+=1
            if large_apply.age in range(20,51) and large_apply.credit =='Y':
                age_25_credit+=1
                
                custom_type = get_custom_type(large_apply)
#                 print large_apply.custom
#                 print custom_type
                
                if(custom_type==1):
                    age_25_credit_one+=1
                if(custom_type==2):
                    age_25_credit_two+=1
                if(custom_type==3):
                    age_25_credit_three+=1
                
            if large_apply.status is not None:
                zx_submit+=1
            if large_apply.policy_id:
                zx_success+=1
                if large_apply.age in range(25,47):
                    zx_effective+=1
               
            loan_set=get_loan_company(lower,upper,large_apply.id)
            if loan_set:
                
                if 'FDB' in loan_set:
                    loan_fdb+=1
                if 'BX' in loan_set:
                    loan_bx+=1
                if 'ZY' in loan_set:
                    loan_zy+=1
            
            
        if dict_inner.get('small',''): 
            small_loan+=1
            small_apply=dict_inner.get('small','')
            if small_apply.age in range(20,51):
                age_25+=1
            if small_apply.age in range(20,51) and small_apply.credit =='Y':
                age_25_credit+=1
                custom_type = get_custom_type(small_apply)
#                 print small_apply.custom
#                 print json.loads(small_apply.custom).get(u'信用卡')
#                 print custom_type
                
                if(custom_type==1):
                    age_25_credit_one+=1
                if(custom_type==2):
                    age_25_credit_two+=1
                if(custom_type==3):
                    age_25_credit_three+=1
                    
            if small_apply.status is not None:
                zx_submit+=1
            if small_apply.policy_id:
                zx_success+=1
                if small_apply.age in range(25,47):
                    zx_effective+=1
            
            loan_set=get_loan_company(lower,upper,small_apply.id)
            if loan_set:
                
                if 'FDB' in loan_set:
                    loan_fdb+=1
                if 'BX' in loan_set:
                    loan_bx+=1
                if 'ZY' in loan_set:
                    loan_zy+=1
                    
#         sql='select * from t_loan_mobiles where create_time > \'%s\' and create_time < \'%s\' ' % (lower,upper)
#         mobile_list = db_conn.query(sql)
#         if mobile_list:
#             submit_phone+=1
        submit_phone+=1
        sql='select * from t_loan_mobiles where verify_time > \'%s\' and verify_time < \'%s\' and mobile = \'%s\' ' % (lower,upper,mobile)
        mobile_list = db_conn.query(sql)
        if mobile_list:
            submit_captcha+=1
        
#     result=coreutils.FancyDict()
#     result.submit_phone=submit_phone
#     result.submit_captcha=submit_captcha
#     result.submit_record=submit_record
#     result.large_loan=large_loan
#     result.small_loan=small_loan
#     result.age_25=age_25
#     result.age_25_credit=age_25_credit
#     result.zx_submit=zx_submit
#     result.zx_success=zx_success
#     result.age_25_credit_one=age_25_credit_one
#     result.age_25_credit_two=age_25_credit_two
#     result.age_25_credit_three=age_25_credit_three
    
    data_list=[]
    
    data_list.append(submit_phone)
    data_list.append(submit_captcha)
    data_list.append(submit_record)
    data_list.append(large_loan)
    data_list.append(small_loan)
    data_list.append(age_25)
    data_list.append(age_25_credit)
    data_list.append(age_25_credit_one)
    data_list.append(age_25_credit_two)
    data_list.append(age_25_credit_three)
    data_list.append(loan_fdb)
    data_list.append(loan_bx)
    data_list.append(loan_zy)
    data_list.append(zx_effective)
    data_list.append(zx_submit)
    data_list.append(zx_success)
    return data_list
    
    
    
def get_loan_company(lower,upper,record_id):
    sql='select * from t_loan_results where create_time > \'%s\' and create_time < \'%s\' and record_id = \'%s\'  and loan_status in (0,3,4,5)' % (lower,upper,record_id)
    
    loan_list = db_conn.query(sql)
    loan_set=set()
    if loan_list:
        
        for loan in loan_list:
            
            if loan.loan_com=='FDB' and loan.loan_status==0:
                loan_set.add(loan.loan_com)
            if loan.loan_com=='ZY' and loan.loan_status==0:
                loan_set.add(loan.loan_com)
            if loan.loan_com=='BX' and loan.loan_status in [3,4,5]:
                loan_set.add(loan.loan_com)
                
    return loan_set
            
    
def write_excel(file_path, data_list):
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'工作表1')
        row = 0
        ws.write(row, 0, u'日期')
        ws.write(row, 1, u'渠道')
        ws.write(row, 2, u'UV')
        ws.write(row, 3, u'提交手机号')
        ws.write(row, 4, u'提交验证码')
        ws.write(row, 5, u'提交贷款')
        ws.write(row, 6, u'大额贷款')
        ws.write(row, 7, u'非大额贷款')
        ws.write(row, 8, u'25-50周岁')
        ws.write(row, 9, u'25-50周岁&有信用卡')
        ws.write(row, 10, u'25-50周岁&有信用卡&车房保单只有其一')
        ws.write(row, 11, u'25-50周岁&有信用卡&车房保单只有其二')
        ws.write(row, 12, u'25-50周岁&有信用卡&车房保单全有')
        ws.write(row, 13, u'飞单保')
        ws.write(row, 14, u'百姓')
        ws.write(row, 15, u'肇煜')
        
        ws.write(row, 16, u'赠险提交数')
        ws.write(row, 17, u'成功赠险数')
        ws.write(row, 18, u'有效赠险')
        row = 1

        for result in data_list:
            col = 0
            for item in result:
                ws.write(row, col, item)
                col += 1
            row += 1

        wb.save(file_path)


def merge_list(date_list_perfix,date_list):
    new_list=date_list_perfix+date_list
    list=[]
    list.append(new_list)
    return list
    
    

# lower='2018-01-02'
# upper='2018-01-03'  
#     
# subchannel='duibahkjcpc1_htlj_new'


# subchannel_set = set() 
# subchannel_set.add('bxmmt1_htlj_new')




def get_uv(lower,subchannel,key_arg):
        redis_conn=dict(host='172.26.36.94',port=6379,db=1,password='heiniu!slave')
        redis_instance=redis.StrictRedis(**redis_conn)
        today_str = lower
        hash_name = today_str + '_' + 'loan_count_v3'+ '_' +subchannel
        key = key_arg
        user_list = []
        value = redis_instance.hget(hash_name, key)
        if value:
            user_list = cPickle.loads(value)
            return len(user_list)
        else:
            return 0



import datetime
lower=datetime.datetime(2018,01,28)
all_date_list=[]

for i in range(1,4):
    lower=lower+datetime.timedelta(days = 1)
    upper=lower+datetime.timedelta(days = 1)
    lower_str=lower.strftime('%Y-%m-%d')
    upper_str=upper.strftime('%Y-%m-%d')
    print lower_str,upper_str
    subchannel_set=get_subchnnel(lower_str,upper_str)
    
    for subchannel in subchannel_set:
        print subchannel
        records_in_dict=get_records_by_subchannel_in_dict(lower_str,upper_str,subchannel)
        data_list=stats_by_subchannel_in_list(records_in_dict,lower_str,upper_str)
        date_list_perfix=[]
        date_list_perfix.append(lower_str)
        date_list_perfix.append(subchannel)
        uv= get_uv(lower_str,subchannel,'index_page')
        date_list_perfix.append(uv)
        all_date_in_subchannel=date_list_perfix+data_list
        all_date_list.append(all_date_in_subchannel)
    
dir = os.path.dirname(os.path.realpath(__file__))
write_excel(dir+'/date'+db_name+'.xls',all_date_list)
 
 
 

        
 
 
 
#(1)渠道校验，无
#(2)提交手机号，提交验证码
#select * from t_loan_records where create_time > '2018-01-02' and create_time < '2018-01-03' and subchannel='wowzfcpczfb1_htlj_new'
#select * from t_loan_mobiles where mobile='13363826813'
# (3)25-50周岁&有信用卡&车房保单只有其二
# select * from t_loan_records where create_time > '2018-01-02' and create_time < '2018-01-03' and subchannel='ywdd_iplj_new'
# (4)查询整个非单保：
# select * from t_loan_results where create_time > '2018-01-02' and create_time < '2018-01-03' and loan_status=0 and loan_com='FDB'