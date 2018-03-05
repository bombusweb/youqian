# -*- coding: utf-8 -*-

import json

# {"信用卡": "有", "名下汽车": "无车", "上班族_公积金": "1年以内", "寿险保单": "有", "名下房产": "有房无贷", "上班族_工资发放": "银行转账", "月收入": "1万以上", 
# "期望贷款": "50000", "您的职业": "上班族", "工作时间": "1年以上"}

question_dict = {
            'amount': u'期望贷款',
            'credit':u'信用卡',
            'house': u'名下房产',
            'car': u'名下汽车',
            'occupation': u'您的职业',
            'way': u'上班族_工资发放',
            'salary': u'月收入',
            'fund': u'上班族_公积金',
            'experience': u'工作时间',
            'license': u'私营业主_营业执照',
            'policy': u'寿险保单',
            
        }
    
question_item_dict={
        'house': {'Y': u'有', 'N': u'没有'},
        'car': {'Y': u'有', 'N': u'没有'},
        'occupation': {'A': u'上班族', 'B': u'公务员', 'C': u'私营业主'},
        'way': {'A': u'银行转账', 'B': u'现金发放'},
        'salary': {'A': u'5千以下', 'B': u'5千-1万', 'C': u'1万以上'},
        'fund': {'C': u'1年以内', 'B': u'1年以上', 'A': u'无公积金'},
        'experience': {'A': u'6个月内', 'B': u'12个月内', 'C': u'1年以上'},
        'license': {'A': u'1年以内', 'B': u'1年以上'},
        'policy': {'Y': u'有', 'N': u'没有'},
    }


def get_loan_apply_item_fillin(amount='500',occupation='A',salary='A',experience='A',way='A',fund='A',license='Y'):
    custom_dict = {
        question_dict['amount']: amount,
        question_dict['occupation']: question_item_dict['occupation'][occupation],
        question_dict['salary']: question_item_dict['salary'][salary],
    }
    if occupation == 'A':
        _custom_dict = {
            question_dict['way']: question_item_dict['way'][way],
            question_dict['fund']: question_item_dict['fund'][fund],
            question_dict['experience']: question_item_dict['experience'][experience],
        }
    elif occupation == 'B':
        _custom_dict = {
            question_dict['experience']: question_item_dict['experience'][experience],
        }
    elif occupation == 'C':
        _custom_dict = {
            question_dict['license']: question_item_dict['license'][license],
        }
    custom_dict.update(_custom_dict)
    return custom_dict

def get_loan_apply_item_perfected(credit='Y',policy='Y',house='Y',car='Y'):
    custom_dict = {
        question_dict['credit']: question_item_dict['credit'][credit],
        question_dict['policy']: question_item_dict['policy'][policy],
        question_dict['house']: question_item_dict['house'][house],
        question_dict['car']: question_item_dict['car'][car]
    }
    return custom_dict

def  get_custom_value(custom):
    
    occupation=''
    way=''
    salary=''
    fund=''
    experience=''
    license=''
    
    house=''
    policy=''
    car=''
    
    if custom.get(question_dict['occupation'],''):
        if custom.get(question_dict['occupation'],'') == question_item_dict['occupation']['A']:
            occupation = 'A'
                
            if custom.get(question_dict['way'],'') == question_item_dict['way']['A']:
                way = 'A'
            elif custom.get(question_dict['way'],'') == question_item_dict['way']['B']:
                way = 'B'
                    
            if custom.get(question_dict['salary'],'') == question_item_dict['salary']['C']:
                salary = 'C'
            elif  custom.get(question_dict['salary'],'') == question_item_dict['salary']['B']:
                salary = 'B'
            elif  custom.get(question_dict['salary'],'') == question_item_dict['salary']['A']:
                salary = 'A'
                
            if custom.get(question_dict['fund'],'') == question_item_dict['fund']['C']:
                fund = 'C'
            elif  custom.get(question_dict['fund'],'') == question_item_dict['fund']['B']:
                fund = 'B'
            elif  custom.get(question_dict['fund'],'') == question_item_dict['fund']['A']:
                fund = 'A'
                    
            if custom.get(question_dict['experience'],'') == question_item_dict['experience']['A']:
                experience = 'A'
            elif  custom.get(question_dict['experience'],'') == question_item_dict['experience']['B']:
                experience = 'B'
            elif  custom.get(question_dict['experience'],'') == question_item_dict['experience']['C']:
                experience = 'C'
                      
        elif custom.get(question_dict['occupation'],'') == question_item_dict['occupation']['B']:
            occupation = 'B'
            
            if custom.get(question_dict['salary'],'') == question_item_dict['salary']['C']:
                salary = 'C'
            elif  custom.get(question_dict['salary'],'') == question_item_dict['salary']['B']:
                salary = 'B'
            elif  custom.get(question_dict['salary'],'') == question_item_dict['salary']['A']:
                salary = 'A'
                
            if custom.get(question_dict['experience'],'') == question_item_dict['experience']['A']:
                experience = 'A'
            elif  custom.get(question_dict['experience'],'') == question_item_dict['experience']['B']:
                experience = 'B'
            elif  custom.get(question_dict['experience'],'') == question_item_dict['experience']['C']:
                experience = 'C'
    
        elif custom.get(question_dict['occupation'],'') == question_item_dict['occupation']['C']:
            occupation = 'C'
            
            if custom.get(question_dict['salary'],'') == question_item_dict['salary']['C']:
                salary = 'C'
            elif  custom.get(question_dict['salary'],'') == question_item_dict['salary']['B']:
                salary = 'B'
            elif  custom.get(question_dict['salary'],'') == question_item_dict['salary']['A']:
                salary = 'A'
                
            if custom.get(question_dict['license'],'') == question_item_dict['license']['A']:
                license = 'A'
            elif custom.get(question_dict['license'],'') == question_item_dict['license']['B']:
                license = 'B'
    
    if custom.get(question_dict['house'],''):
        if custom.get(question_dict['house'],'') == question_item_dict['house']['Y']:
            house='Y'
        elif custom.get(question_dict['house'],'') == question_item_dict['house']['N']:
            house='N'
        
    if custom.get(question_dict['policy'],''):
        if custom.get(question_dict['policy'],'') == question_item_dict['policy']['Y']:
            policy='Y'
        elif custom.get(question_dict['policy'],'') == question_item_dict['policy']['N']:
            policy='N'
  
    if custom.get(question_dict['car'],''):
        if custom.get(question_dict['car'],'') == question_item_dict['car']['Y']:
            car='Y'
        elif custom.get(question_dict['car'],'') == question_item_dict['car']['N']:
            car='N'
            
    value_in_custom_in_dict={}
    value_in_custom_in_dict['occupation']=occupation
    value_in_custom_in_dict['way']=way
    value_in_custom_in_dict['salary']=salary
    value_in_custom_in_dict['fund']=fund
    value_in_custom_in_dict['experience']=experience
    value_in_custom_in_dict['license']=license
    value_in_custom_in_dict['house']=house
    value_in_custom_in_dict['policy']=policy
    value_in_custom_in_dict['car']=car
    
    return value_in_custom_in_dict
    
    
            
def  get_record_value_in_dict(record,step):
    value_in_dict={}
    value_in_dict['amount']=str(record.amount)
    value_in_dict['name']=record.name
    value_in_dict['birth']=record.birth
    value_in_dict['sex']=record.sex
    value_in_dict['credit']=record.credit
    custom_in_dict=json.loads(record.custom)
    value_in_custom_in_dict=get_custom_value(custom_in_dict)
    if value_in_custom_in_dict:
        value_in_dict.update(value_in_custom_in_dict)
    keys_in_second=['credit','policy','house','car']
    value_in_second={}
    value_in_first={}
    for key, value in value_in_dict.items():
        if step=='second':
            if key in keys_in_second:
                value_in_second[key]=value
        else:
            if key not in keys_in_second:
                value_in_first[key]=value
            
    if step=='second':
        return value_in_second
    else:
        return value_in_first
        
    
# "data": {
#     "amount": "500",
#     "name": "测试",
#     "birth": "1988-01-01",
#     "sex": "M",
#     "occupation": "B",
#     "way": "",
#     "salary": "A",
#     "fund": "",
#     "experience": "C",
#     "license": ""
#   }
# 
# {
#     credit: 'Y',
#     policy: 'Y',
#     house: 'N',
#     car: 'N'
# }

class CompanyInSmallLoan(object):
    
    data=[]
    data_1={
        "name": "pinganpuhui",
        "link": "https://www.heiniubao.com/activity/gopaph2",
        "logo": "http://localhost:8082/static/upload/images/logos/wap-loan-pinganpuhui.png",
        "title": u"平安普惠",
        "amount": u"额度,10000,300000",
        "desc": [u"放款快", u"无抵押"],
        "button_text": u"立即申请"
    }
    data_2={
        "name": "rong360",
        "link": "https://www.heiniubao.com/activity/go_rong360_1",
        "logo": "http://localhost:8082/static/upload/images/logos/wap-loan-rong360.png",
        "title": u"融360",
        "amount": u"额度,2000,500000",
        "desc": [u"额度大", u"实名手机"],
        "button_text": u"立即申请"
    }
    data_3={
        "name": "sudaizhijia",
        "link": "https://www.heiniubao.com/activity/gosudaizhijia1",
        "logo": "http://localhost:8082/static/upload/images/logos/wap-loan-sudaizhijia.png",
        "title": u"速贷之家",
        "amount": u"额度,1000,50000",
        "desc": [u"放款快", u"利率低"],
        "button_text": u"立即申请"
    }
    
    data.append(data_1)
    data.append(data_2)
    data.append(data_3)
    
def class_to_dict(dict_in_class):
    dict={}
    for key, value in dict_in_class.__dict__.items():
        if key in ('__module__','__dict__','__weakref__','__doc__','banner_1','banner_2','banner_3','nav_1','nav_2','nav_3','data_1','data_2','data_3'):
            pass
        else:
            dict[key]=value
    return dict


def get_company_in_samll_loan():
    dict=class_to_dict(CompanyInSmallLoan)
    dict['status']=0
    dict['msg']=''
    return json.dumps(dict,ensure_ascii=False)
    
import torndb

db_conn = torndb.Connection(
                        host = '47.94.206.52',
                        database = 'heiniu',
                        user = 'root',
                        password = 'wxf-1983-720985')
sql_exp='select * from t_wx_loan_records where user_id="1"'
loan_record=db_conn.query(sql_exp)[0]
is_large_loan = int(float(loan_record.amount)) in range(5000, 500001) and int(loan_record.age) in range(28, 51) and loan_record.credit == 'Y'
print is_large_loan

