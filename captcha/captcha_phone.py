#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import redis
import datetime
import random
import logging
import hashlib

import redis_interface

ERROR_SUCCESS = 0

# login errors begin with 100001
ERROR_INVALID_EMAIL         = 100001
ERROR_INCORRECT_PASSWORD    = 100002
ERROR_EMAIL_NOT_REGISTERD   = 100003
ERROR_EAMIL_REGISTERD       = 100004
ERROR_INVALID_ID            = 100005
ERROR_INVALID_PHONE         = 100006
ERROR_PHONE_REGISTERD       = 100007
ERROR_PHONE_NOT_REGISTERD   = 100008
ERROR_CAPTCHA_GENERATED     = 100009
ERROR_CAPTCHA_LIMIT         = 100010
ERROR_CAPTCHA_FAILED        = 100011
ERROR_INVALID_USERNAME      = 100012
ERROR_INVALID_LOGIN_TYPE    = 100013
ERROR_UNAUTH_CHANGE_PASS    = 100014
ERROR_INVALID_PASSWORD      = 100015
ERROR_CAPTCHA_LIMIT_TIME    = 100016
ERROR_PASSWORD_TRY_LIMIT    = 100017
ERROR_CAPTCHA_TRY_LIMIT     = 100018
ERROR_INVALID_HTTP_REFERER  = 100019
ERROR_IP_IN_BLACKLIST       = 100020
ERROR_RANDOM_NUMBER         = 100021

class VerificationInput(object):

    def __init__(self):
        super(VerificationInput, self).__init__()

        self.re_name = re.compile('^[a-zA-z][a-zA-Z0-9_]{2,9}$')
        self.re_password = re.compile('^[.\n]*$')
        # 涉及到发短信验证码，校验手机号的正则改为1开头的11位数字，之前的2-9的也可以
        self.re_phone = re.compile('^1\d{10}$')
        self.re_email = re.compile('^\w+[-+.\w]*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
        self.re_digit = re.compile('^\d+$')

    @staticmethod
    def instance():
        if not hasattr(VerificationInput, "_instance"):
            # New instance
            VerificationInput._instance = VerificationInput()
        return VerificationInput._instance

    def check_name(self, name):
        return self.re_name.match(name) is not None

    def check_password(self, password):
        return self.re_password.match(password) is not None

    def check_phone(self, phone):
        return self.re_phone.match(phone) is not None

    def check_email(self, email):
        return self.re_email.match(email) is not None

class CaptchaPhone(object):

    def __init__(self, redis_server):
        super(CaptchaPhone, self).__init__()

        self.redis_server = redis_server

        # 验证码多久会被自动清除
        self.captcha_expire = 120
        # 客户端两次请求的最低间隔
        self.limit_time = 60
        # 同一个手机号码每天最多可以请求成功的次数
        self.limit_per_day = 10
        # 同一ip每天最多可以请求的次数
        self.limit_ip_per_day = 20
        # 上面次数的保留时间
        self.limit_expire = 24 * 60 * 60
        # 挑战数保留时间
        self.random_expire = 24 * 60 * 60
        # 挑战数最多可以验证几次
        self.random_valid = 2

        # 同一手机号码尝试错误次数最大限制，防止暴力猜解
        self.max_try_count = 5
        # 错误次数达到限制后多长时间内不再接收对该号码的验证码验证请求
        self.failed_expire = 15 * 60

        lua_scripts = """
            local value = redis.call('GET', KEYS[1])
            value = tonumber(value)
            local total = tonumber(ARGV[1])
            if value == nil or value < total then
                redis.call('INCR', KEYS[1])
                redis.call('EXPIRE', KEYS[1], ARGV[2])
            end
            return value
            """

        self.lua_limit = self.redis_server.register_script(lua_scripts)
        self.input_verification = VerificationInput.instance()

    @staticmethod
    def instance(redis_server):
        if not hasattr(CaptchaPhone, "_instance"):
            # New instance
            CaptchaPhone._instance = CaptchaPhone(redis_server)
        return CaptchaPhone._instance

    def get_limit_key(self, phone):
        today = str(datetime.date.today())
        key = 'captcha_' + today + '_' + phone
        return key

    def gen_random(self):
        l = "abcdef1234567890"
        value = [l[random.randint(0, 15)] for i in xrange(32)]
        value = ''.join(value)
        key = 'captcha_r_' + value
        self.redis_server.set(key, 0)
        self.redis_server.expire(key, self.random_expire)
        logging.info('gen random:%s' % value)
        return value

    def verify_random(self, r):
        key = 'captcha_r_' + r
        value = self.redis_server.get(key)
        if value == None:
            return ERROR_CAPTCHA_LIMIT
        self.redis_server.incr(key)
        # 验证完保留，用户可以不刷新页面再次获取验证码
        value = int(value) + 1
        if value >= self.random_valid:
            logging.info('delete key:%s' % key)
            self.redis_server.delete(key)
        return ERROR_SUCCESS

    def gen_value(self):
        value = random.sample('0123456789', 4)
        return ''.join(value)

    def gen_id(self, phone):
        key = 'captcha_' + phone
        return key

    def get_limit_ip_key(self, remote_ip):
        today = str(datetime.date.today())
        ip_limit_key = 'captcha_' + today + '_' + remote_ip
        return ip_limit_key

    def gen_captcha(self, phone, remote_ip, r):
        logging.info('gen captcha, phone:%s' % phone)

        if not self.input_verification.check_phone(phone):
            return ERROR_INVALID_PHONE, None

        if self.verify_random(r) != ERROR_SUCCESS:
            logging.info('invalid random')
            return ERROR_CAPTCHA_LIMIT, None

        # check limit ip per day. count of calling this interface,
        # not count of calling this interface successful.
        key_limit = self.get_limit_ip_key(remote_ip)
        count = self.lua_limit(
                    keys = [key_limit],
                    args = [self.limit_ip_per_day, self.limit_expire])
        if count != None and count >= self.limit_ip_per_day:
            logging.info('captha reach limit')
            return ERROR_CAPTCHA_LIMIT, None

        key = self.gen_id(phone)
        key_expire = key + '_expire'
        limit_key = self.redis_server.get(key_expire)
        if limit_key != None:
            return ERROR_CAPTCHA_LIMIT_TIME, None

        # check limit per day
        key_limit = self.get_limit_key(phone)
        count = self.lua_limit(
                    keys = [key_limit],
                    args = [self.limit_per_day, self.limit_expire])
        if count != None and count >= self.limit_per_day:
            logging.info('captha reach limit')
            return ERROR_CAPTCHA_LIMIT, None

        value = self.gen_value()
        self.redis_server.set(key, value)
        self.redis_server.expire(key, self.captcha_expire)
        logging.info('key :%s value:%s' % (key, value))

        # set limit
        self.redis_server.set(key_expire, 1)
        self.redis_server.expire(key_expire, self.limit_time)

        return ERROR_SUCCESS, value

    def _gen_failed_limit(self, phone):
        return 'captha_failed_%s' % phone

    def _increase_failed(self, phone):
        # increase failed count
        redis = redis_interface.RedisInterface.instance()
        key = self._gen_failed_limit(phone)
        redis.lock_incr(key, self.max_try_count, self.failed_expire)

    def _check_failed(self, phone):
        redis_db = redis_interface.RedisInterface.instance().redis
        key = self._gen_failed_limit(phone)
        count = redis_db.get(key)
        if count == None:
            count = 0
        count = int(count)
        if count >= self.max_try_count:
            return ERROR_CAPTCHA_TRY_LIMIT
        return ERROR_SUCCESS

    def verify(self, phone, captcha):
        logging.info('verify captcha, phone:%s' % phone)

        error_code = self._check_failed(phone)
        if error_code != ERROR_SUCCESS:
            return error_code

        if not self.input_verification.check_phone(phone):
            return ERROR_INVALID_PHONE

        key = self.gen_id(phone)
        value = self.redis_server.get(key)
        if value != captcha:
            logging.info("stored captcha:%s" % value)
            self._increase_failed(phone)
            return ERROR_CAPTCHA_FAILED
        return ERROR_SUCCESS