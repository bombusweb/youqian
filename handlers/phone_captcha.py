#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import json
from datetime import timedelta

import tornado.gen

import api.dayu.sms
import api.webpower.sms
import db_interface
import world
import base
import chuanglan.sms
from api.manager.smsControl import SmsService
import insurance.table_config
from insurance.common import *
from insurance.base_check import *

import api.captcha.captcha_phone
from api.captcha.captcha_phone import *
import api.token.jwt_token
from api.xianjinka.card import XinJinKaApi

from utils.timeutil import get_today_str, get_now_str

from tornado.web import HTTPError, asynchronous


class HandlerPhoneCaptcha(base.MainHandler):

    def initialize(self):
        super(HandlerPhoneCaptcha, self).initialize()
        self.handler_path = '/gen/phone_captcha'
        self.world_instance = world.World.instance()
        self.redis_server = self.world_instance.redis

    def _log_sms_send_info(self, phone, success=False, sms_name=''):
        logging.info('_log_sms_send_info phone:{}, success:{}'.format(phone, success))
        key_name = 'heiniu:sms_all:{}:{}'.format(sms_name, get_today_str(only_date=True))
        self._incr_key_and_expire(key_name)

        if not success:
            # 记录发送失败数
            key_name = 'heiniu:sms_error:{}:{}'.format(sms_name, get_today_str(only_date=True))
            self._incr_key_and_expire(key_name)

            hour = get_now_str()[:13].replace(' ', '_')
            key_name = 'heiniu:sms_error_hour:{}:{}'.format(sms_name, hour)
            self._incr_key_and_expire(key_name)

    def _incr_key_and_expire(self, key_name):
        logging.info('_log_sms_send_info key_name:{} incr'.format(key_name))
        self.redis_server.incr(key_name, 1)
        self.redis_server.expire(key_name, timedelta(days=REDIS_KEEP_DAYS))

    def check_valid(self):
        logging.info('self.http_referer:{}'.format(self.http_referer))
        if self.http_referer == '':
            return ERROR_INVALID_HTTP_REFERER

        if self.http_referer.find(self.uri) != -1:
            logging.info('referer:%s' % self.http_referer)
            return ERROR_INVALID_HTTP_REFERER

        return ERROR_SUCCESS

    def _parse_chuanglan_result(self, phone, sms_result):
        send_success = False
        try:
            if isinstance(sms_result, dict):
                sms_code = sms_result.get('code', '')
                if sms_code in ['0', 0]:
                    send_success = True
                else:
                    send_success = False
            self._log_sms_send_info(phone, success=send_success, sms_name='chuanglan')
        except:
            logging.error(traceback.format_exc())
        return send_success

    def _parse_webpower_result(self, phone, sms_result):
        send_success = False
        try:
            if isinstance(sms_result, dict):
                sms_status = sms_result.get('status', '')
                # webpower接口会返回类似 {u'status': 1002} 这样的异常代码，这个时候status是数值的
                if isinstance(sms_status, (str, unicode)):
                    sms_status = sms_status.lower()
                if sms_status in ['ok']:
                    send_success = True
                else:
                    send_success = False
            self._log_sms_send_info(phone, success=send_success, sms_name='webpower')
        except:
            logging.error(traceback.format_exc())
        return send_success

    def _get_random_key(self, sms_config_dict):
        all_list = []
        for key, info in sms_config_dict.items():
            tmp_list = []
            for _ in range(info[0]):
                tmp_list.append(key)
            all_list.extend(tmp_list)
        n = random.randint(0, len(all_list) - 1)
        key = all_list[n]
        return key

    @tornado.gen.coroutine
    def _random_sms_send(self, phone, sms_text, webpower_prefix=''):
        sms_config_dict = {
            'webpower': [0, api.webpower.sms.WebPowerSmsService(webpower_prefix), self._parse_webpower_result],
            'chuanglan': [10, chuanglan.sms.SmsChuanglan_New(), self._parse_chuanglan_result]
        }
        random_key = self._get_random_key(sms_config_dict)
        logging.info('_random_sms_send random_key:{}, phone:{}, sms_text:{}'.format(random_key, phone, sms_text))
        _, sms_sender, result_parser_func = sms_config_dict[random_key]
        sms_result = yield sms_sender.send_sms(phone, sms_text)
        result = result_parser_func(phone, sms_result)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def get(self):

        error_code = ERROR_SUCCESS
        error_msg = ''
        captcha = ''

        # only valid request can send message.
        if self.check_valid() == ERROR_SUCCESS:
            phone = self.get_argument('phone')
            r = self.get_argument('r')
            #captcha_type = self.get_argument('type')

            # if captcha_type == '2':
            #     # register check phone
            #     error_code, uid = auth_manager.check_register_phone(phone)
            #     if error_code != ERROR_SUCCESS:
            #         error_msg = get_error_msg(error_code)
            #         param_dict = {
            #             "error_code" : error_code,
            #             "error_msg" : error_msg,
            #         }
            #         text = json.dumps(param_dict)
            #         self.write(text)
            #         return
            # else:
            #     pass
            captcha_manager = api.captcha.captcha_phone.CaptchaPhone.instance(self.redis_server)
            error_code, captcha = captcha_manager.gen_captcha(phone, self.remote_ip, r)
            error_msg = ''

            if captcha != None:
                if self.world_instance.is_tester:
                    logging.info('captcha is:%s' % captcha)
                    error_code = ERROR_SUCCESS
                else:
                    # send sms
                    # 检查用户的http_referer前30个字符中是否有100alpha.com，有的话发默认验证码用蘑菇保
                    if '100alpha.com' in self.http_referer[:30]:
                        sms_text = '【蘑菇保】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                        webpower_prefix = 'mogubao'
                    else:
                        sms_text = '【黑牛保】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                        webpower_prefix = 'custom'
                    yield self._random_sms_send(phone, sms_text, webpower_prefix=webpower_prefix)
                    error_code = ERROR_SUCCESS
        error_msg = self.get_error_msg(error_code, error_msg)
        logging.info('error_code:{}, error_msg:{}'.format(error_code, error_msg))

        if error_code in [ERROR_CAPTCHA_LIMIT, ERROR_CAPTCHA_LIMIT_TIME]:
            error_msg = '您获取验证码过于频繁，请稍候再试'

        param_dict = {
            "error_code" : error_code,
            "error_msg" : error_msg,
        }

        if self.world_instance.is_tester:
            param_dict['captcha'] = captcha

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)


class VerifyPhoneCaptcha(HandlerPhoneCaptcha):
    def initialize(self):
        super(VerifyPhoneCaptcha, self).initialize()
        self.handler_path = '/verify/phone_captcha'

    def get(self):
        phone = self.get_argument('phone')
        captcha = self.get_argument('captcha')
        captcha_manager = api.captcha.captcha_phone.CaptchaPhone.instance(self.redis_server)
        error_code = captcha_manager.verify(phone, captcha)
        jwt_token = ''
        if error_code != ERROR_SUCCESS:
            error_code = ERROR_CAPTCHA
            logging.error('verify captcha fail, phone:%s, captcha: %s' % (phone, captcha))
        else:
            jwt_cli = api.token.jwt_token.JWTToken()
            jwt_token = jwt_cli.gen_jwt_token(phone)

        param_dict = {
            "error_code" : error_code,
            "token" : jwt_token
        }

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)


class HandlerXinJinKaPhoneCaptcha(base.MainHandler):

    def initialize(self):
        super(HandlerXinJinKaPhoneCaptcha, self).initialize()
        self.handler_path = '/gen/phone_xjk_captcha'
        self.world_instance = world.World.instance()
        self.redis_server = self.world_instance.redis

    def check_valid(self):
        logging.info('self.http_referer:{}'.format(self.http_referer))
        # # 测试环境下，暂时不判断http_referer
        # if self.world_instance.is_tester:
        #     return ERROR_SUCCESS
        if self.http_referer == '':
            return ERROR_INVALID_HTTP_REFERER

        if self.http_referer.find(self.uri) != -1:
            logging.info('referer:%s' % self.http_referer)
            return ERROR_INVALID_HTTP_REFERER

        return ERROR_SUCCESS

    @tornado.gen.coroutine
    def get(self):

        error_code = ERROR_SUCCESS
        error_msg = ''
        captcha = ''
        is_new_user = True

        # only valid request can send message.
        if self.check_valid() == ERROR_SUCCESS:
            phone = self.get_argument('phone')
            r = self.get_argument('r')
            # 请求现金卡验证码
            if self.world_instance.is_tester:
                api = XinJinKaApi(is_test=True)
            else:
                api = XinJinKaApi(is_test=False)
            is_new_user = yield api.get_reg_code(phone)
        if not is_new_user:
            error_code = 1
            error_msg = '您已注册过现金卡，无需输入验证码'
        param_dict = {
            "error_code" : error_code,
            "error_msg" : error_msg,
        }

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)


class HeiNiuYouQianPhoneCaptcha(HandlerPhoneCaptcha):

    def initialize(self):
        super(HeiNiuYouQianPhoneCaptcha, self).initialize()
        self.handler_path = '/gen/phone_hnyq_captcha'

    @tornado.gen.coroutine
    def get(self):

        error_code = ERROR_SUCCESS
        error_msg = ''
        captcha = ''

        # only valid request can send message.
        if self.check_valid() == ERROR_SUCCESS:
            phone = self.get_argument('phone')
            r = self.get_argument('r')

            captcha_manager = api.captcha.captcha_phone.CaptchaPhone.instance(self.redis_server)
            error_code, captcha = captcha_manager.gen_captcha(phone, self.remote_ip, r)
            error_msg = ''

            if captcha != None:
                if self.world_instance.is_tester:
                    logging.info('captcha is:%s' % captcha)
                    error_code = ERROR_SUCCESS
                else:
                    # send sms
                    # sms_text = '【黑牛有钱】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    # sms_sender = chuanglan.sms.SmsChuanglan_New()
                    # sms_result = yield sms_sender.send_sms(phone, sms_text)
                    # self._parse_chuanglan_result(phone, sms_result)
                    # error_code = ERROR_SUCCESS

                    # send sms
                    sms_text = '【黑牛有钱】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    # sender = api.dayu.sms.SmsSender()
                    # sender.send_sms(phone, "SMS_8951296", sms_text)
                    yield self._random_sms_send(phone, sms_text, webpower_prefix='heiniuyouqian')
                    error_code = ERROR_SUCCESS
        logging.info('error_code:{}, error_msg:{}'.format(error_code, error_msg))
        error_msg = self.get_error_msg(error_code, error_msg)

        if error_code in [ERROR_CAPTCHA_LIMIT, ERROR_CAPTCHA_LIMIT_TIME]:
            error_msg = '您获取验证码过于频繁，请稍候再试'

        param_dict = {
            "error_code": error_code,
            "error_msg": error_msg,
        }

        if self.world_instance.is_tester:
            param_dict['captcha'] = captcha

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)


class HeiNiuShangChengPhoneCaptcha(HandlerPhoneCaptcha):

    def initialize(self):
        super(HeiNiuShangChengPhoneCaptcha, self).initialize()
        self.handler_path = '/gen/phone_shop_captcha'

    @tornado.gen.coroutine
    def get(self):

        error_code = ERROR_SUCCESS
        error_msg = ''
        captcha = ''

        # only valid request can send message.
        if self.check_valid() == ERROR_SUCCESS:
            phone = self.get_argument('phone')
            r = self.get_argument('r')

            captcha_manager = api.captcha.captcha_phone.CaptchaPhone.instance(self.redis_server)
            error_code, captcha = captcha_manager.gen_captcha(phone, self.remote_ip, r)
            error_msg = ''

            if captcha != None:
                if self.world_instance.is_tester:
                    logging.info('captcha is:%s' % captcha)
                    error_code = ERROR_SUCCESS
                else:
                    # send sms
                    sms_text = '【黑牛商城】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    sms_sender = chuanglan.sms.SmsChuanglan_New()
                    sms_result = yield sms_sender.send_sms(phone, sms_text)
                    self._parse_chuanglan_result(phone, sms_result)
                    error_code = ERROR_SUCCESS

                    # # send sms
                    # sms_text = '【黑牛商城】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    # # sender = api.dayu.sms.SmsSender()
                    # # sender.send_sms(phone, "SMS_8951296", sms_text)
                    # yield self._random_sms_send(phone, sms_text, webpower_prefix='heiniuyouqian')
                    # error_code = ERROR_SUCCESS
        logging.info('error_code:{}, error_msg:{}'.format(error_code, error_msg))
        error_msg = self.get_error_msg(error_code, error_msg)

        if error_code in [ERROR_CAPTCHA_LIMIT, ERROR_CAPTCHA_LIMIT_TIME]:
            error_msg = '您获取验证码过于频繁，请稍候再试'

        param_dict = {
            "error_code": error_code,
            "error_msg": error_msg,
        }

        if self.world_instance.is_tester:
            param_dict['captcha'] = captcha

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)


class NoHeiNiuPhoneCaptcha(HandlerPhoneCaptcha):

    def initialize(self):
        super(NoHeiNiuPhoneCaptcha, self).initialize()
        self.handler_path = '/gen/phone_noheiniu_captcha'

    @tornado.gen.coroutine
    def get(self):

        error_code = ERROR_SUCCESS
        error_msg = ''
        captcha = ''

        # only valid request can send message.
        if self.check_valid() == ERROR_SUCCESS:
            phone = self.get_argument('phone')
            r = self.get_argument('r')

            captcha_manager = api.captcha.captcha_phone.CaptchaPhone.instance(self.redis_server)
            error_code, captcha = captcha_manager.gen_captcha(phone, self.remote_ip, r)
            error_msg = ''

            if captcha != None:
                if self.world_instance.is_tester:
                    logging.info('captcha is:%s' % captcha)
                    error_code = ERROR_SUCCESS
                else:
                    # send sms
                    sms_text = '【专享活动】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    sms_sender = chuanglan.sms.SmsChuanglan_New()
                    sms_result = yield sms_sender.send_sms(phone, sms_text)
                    self._parse_chuanglan_result(phone, sms_result)
                    error_code = ERROR_SUCCESS

                    # # send sms
                    # sms_text = '【黑牛商城】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    # # sender = api.dayu.sms.SmsSender()
                    # # sender.send_sms(phone, "SMS_8951296", sms_text)
                    # yield self._random_sms_send(phone, sms_text, webpower_prefix='heiniuyouqian')
                    # error_code = ERROR_SUCCESS
        logging.info('error_code:{}, error_msg:{}'.format(error_code, error_msg))
        error_msg = self.get_error_msg(error_code, error_msg)

        if error_code in [ERROR_CAPTCHA_LIMIT, ERROR_CAPTCHA_LIMIT_TIME]:
            error_msg = '您获取验证码过于频繁，请稍候再试'

        param_dict = {
            "error_code": error_code,
            "error_msg": error_msg,
        }

        if self.world_instance.is_tester:
            param_dict['captcha'] = captcha

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)


class MoGuBaoPhoneCaptcha(HandlerPhoneCaptcha):

    def initialize(self):
        super(MoGuBaoPhoneCaptcha, self).initialize()
        self.handler_path = '/gen/phone_mgb_captcha'

    @tornado.gen.coroutine
    def get(self):

        error_code = ERROR_SUCCESS
        error_msg = ''
        captcha = ''

        # only valid request can send message.
        if self.check_valid() == ERROR_SUCCESS:
            phone = self.get_argument('phone')
            r = self.get_argument('r')

            captcha_manager = api.captcha.captcha_phone.CaptchaPhone.instance(self.redis_server)
            error_code, captcha = captcha_manager.gen_captcha(phone, self.remote_ip, r)
            error_msg = ''

            if captcha != None:
                if self.world_instance.is_tester:
                    logging.info('captcha is:%s' % captcha)
                    error_code = ERROR_SUCCESS
                else:
                    # send sms
                    sms_text = '【蘑菇保】您的验证码是{}。如非本人操作，请忽略此短信。'.format(captcha)
                    webpower_prefix = 'mogubao'
                    yield self._random_sms_send(phone, sms_text, webpower_prefix=webpower_prefix)
                    error_code = ERROR_SUCCESS
        logging.info('error_code:{}, error_msg:{}'.format(error_code, error_msg))
        error_msg = self.get_error_msg(error_code, error_msg)

        if error_code in [ERROR_CAPTCHA_LIMIT, ERROR_CAPTCHA_LIMIT_TIME]:
            error_msg = '您获取验证码过于频繁，请稍候再试'

        param_dict = {
            "error_code": error_code,
            "error_msg": error_msg,
        }

        if self.world_instance.is_tester:
            param_dict['captcha'] = captcha

        text = json.dumps(param_dict)
        text = json.loads(text)
        self.write(text)