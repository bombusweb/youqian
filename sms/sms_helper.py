# -*- coding: utf-8 -*-

import json
import time
import urllib2

CHUANGLAN_NEW = {
    'account': 'N2042705',
    'password': 'caXTqGpD9V0591'
}

def do_try(func, times, sleep_time=5):
    try_num = 0
    max_try_num = times
    while try_num < max_try_num:
        try:
            result = func()
            return result
        except:
            try_num += 1
            time.sleep(sleep_time)


class SmsChuanglan_New(object):
    def __init__(self):
        # 服务地址
        self.host = "https://vsms.253.com"

        # 端口号
        self.port = 80

        # 版本号
        self.version = "v1.1"

        # 查账户信息的URI
        self.balance_get_uri = "/msg/balance/json"

        # 智能匹配模版短信接口的URI
        self.sms_send_uri = "/msg/send/json"

        self.sms_param_uri = "/msg/variable/json"

        self.account = CHUANGLAN_NEW['account']
        self.password = CHUANGLAN_NEW['password']

    def parse_balance(self):
        link = self.host + self.balance_get_uri
        params = {
            "account": self.account,
            "password": self.password
        }
        data = json.dumps(params)
        request = urllib2.Request(link)
        request.add_header('Content-Type', 'application/json;charset=utf-8')
        response = urllib2.urlopen(request, data=data)
        return json.loads(response.read())['balance']

    def send_sms(self, mobile, text):
        link = self.host + self.sms_send_uri
        param_list = {
            'account': self.account,
            'password': self.password,
            'msg': text,
            'phone': mobile,
            'sendtime': '',
            'report': "false",
            'extend': ''
        }
        params = json.dumps(param_list)
        request = urllib2.Request(link)
        request.add_header('Content-Type', 'application/json;charset=utf-8')
        response = urllib2.urlopen(request, data=params)
        result = None
        try:
            result = json.loads(response.read())
        except:
            pass
        return result

    def get_user_balance(self):
        """
        取账户余额
        """
        return do_try(self.parse_balance, times=5)


if __name__ == '__main__':
    sender = SmsChuanglan_New()
    message = "id为的广告点击已达上限80%，实时点击为，请及时关注"
    sender.send_sms('13691036309', message)
   