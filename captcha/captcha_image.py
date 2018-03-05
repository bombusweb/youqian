# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import traceback

import tornado.web
import tornado.gen
import tornado.httpclient

import utils.httputils
import world

IMAGE_CAPTCHA_SERVER_ADDRESS = 'http://120.55.88.54/image-captcha-server'

class VerifyStatus(object):
    VERIFY_SUCCESS = 0
    ERROR_PARAM = 1
    VERIFY_FAILED= 2
    VERIFY_TOO_FAST = 3
    EXPIRE = 4

    MESSAGES = {
        ERROR_PARAM: u'参数错误',
        VERIFY_FAILED: u'验证码错误',
        VERIFY_SUCCESS: u'验证成功',
        VERIFY_TOO_FAST: u'操作过于频繁，请稍后再试',
        EXPIRE: u'验证码已经过期，请重新输入',
    }

class ImageCaptcha(object):
    @staticmethod
    def instance():
        if not hasattr(ImageCaptcha, '_instance'):
            ImageCaptcha._instance = ImageCaptcha()

        return ImageCaptcha._instance

    def __init__(self):
        self._get_key_url = '%s/getkey' % IMAGE_CAPTCHA_SERVER_ADDRESS
        self._verify_code_url = '%s/verify?key={}&code={}' % IMAGE_CAPTCHA_SERVER_ADDRESS
        self._show_image_url = '%s/showimage?key={}' % IMAGE_CAPTCHA_SERVER_ADDRESS

        # 需要图片验证码的渠道
        self._image_captcha_channels = ['ddwxservice', 'pawxservice']
        # 校验次数的阈值
        self._threshold = 1000
        self._redis_key_prefix = 'imagecaptcha'
        self._user_expire_time = 3 * 60
        self._token_expire_time = 15 * 60

        self._md5_salt = 'Heiniu1003!0(xF#d9$'

        self._redis = world.World.instance().redis

    @tornado.gen.coroutine
    def get_key(self):

        url = self._get_key_url
        error_no = -1
        key = None
        response_str = yield utils.httputils.async_http_fetch(url)
        if not response_str:
            raise tornado.gen.Return(None)

        try:
            response = json.loads(response_str)

            error_no = int(response['error_no'])
            key = response['key']
        except Exception as e:
            logging.error(e)

        if error_no == 0 and key:
            raise tornado.gen.Return(key)
        else:
            raise tornado.gen.Return(None)

    @tornado.gen.coroutine
    def verify(self, ip, user_agent, key, code):
        count = self._get_verify_count(ip, user_agent, key)
        if count > self._threshold:
            logging.info('[image captcha] limit threshold. ip="{}", user_agent="{}"'.format(ip, user_agent))
            raise tornado.gen.Return(VerifyStatus.VERIFY_TOO_FAST)

        url = self._verify_code_url.format(key, code)

        error_no = -1
        try:
            response_str = yield utils.httputils.async_http_fetch(url)
            response = json.loads(response_str)
            error_no = response['error_no']
        except Exception as e:
            traceback.print_exc()
            logging.error(e)
            raise tornado.gen.Return(VerifyStatus.VERIFY_FAILED)

        if error_no == 0:
            status = VerifyStatus.VERIFY_SUCCESS
        else:
            status = VerifyStatus.VERIFY_FAILED

        raise tornado.gen.Return(status)


    def _get_verify_count(self, ip, user_agent, key):
        """
        获得缓存中用户操作的次数
        """
        redis_postfix_raw = ip + '-' + user_agent

        md5 = hashlib.md5()
        md5.update(redis_postfix_raw)
        redis_postfix = md5.hexdigest()

        redis_key = self._redis_key_prefix + redis_postfix

        count = self._redis.get(redis_key)

        logging.info('[image captcha] key is {}. raw redis postfix is {}. redis key is {}. count is {}'.format(
            key, redis_postfix_raw, redis_key, count)
        )
        if count:
            self._redis.incrby(redis_key, 1)
            count = int(count) + 1
        else:
            expire_time = self._user_expire_time
            count = 1
            self._redis.set(redis_key, count, ex=expire_time)

        return count

    @tornado.gen.coroutine
    def show_image(self, key):
        url = self._show_image_url.format(key)
        response = yield utils.httputils.async_http_fetch(url)
        raise tornado.gen.Return(response)

    def generate_token(self, key):
        """
        验证成功后，生成一个token返回给前端，并且存在redis中
        """
        md5 = hashlib.md5()
        md5.update(key + self._md5_salt)
        token = md5.hexdigest()


        return token

    def is_valid_token(self, captcha_key, token_in_param):
        if not token_in_param:
            return False

        token = self.generate_token(captcha_key)
        if token != token_in_param:
            logging.warn('[image captcha] token not equal. token generated is {}, token in param is {}'.format(
                token, token_in_param
            ))
            return False

        redis_key = self.generate_redis_token_key(captcha_key)
        token_in_redis = self._redis.get(redis_key)
        if token_in_redis != token_in_param:
            logging.warn('[image captcha] token not equal. token in redis is {}, token in param is {}'.format(
                token_in_redis, token_in_param
            ))
            return False

        self._redis.delete(redis_key)
        return True

    def generate_redis_token_key(self, captcha_key):
        return self._redis_key_prefix + '-' + captcha_key

    def set_token_in_redis(self, redis_key, token):
        redis = world.World.instance().redis
        redis.set(redis_key, token, ex=self._token_expire_time)

    def is_need_image_captcha(self, channel):
        return channel in self._image_captcha_channels



