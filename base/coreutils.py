# -*- coding: utf-8 -*-
import random
import re
import string
import uuid
import json
import socket
import struct
import datetime
import logging
import urllib
import smtplib
from email.mime.text import MIMEText


if type('') is not type(b''):
    bytes_type = bytes
    unicode_type = str
    basestring_type = str
else:
    bytes_type = str
    unicode_type = unicode
    basestring_type = basestring

_UTF8_TYPES = (bytes_type, type(None))
_TO_UNICODE_TYPES = (unicode_type, type(None))


def utf8(text):
    """
        Converts a string argument to a byte string.

        If the argument is already a byte string or None, it is returned unchanged.
        Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(text, _UTF8_TYPES):
        return text
    assert isinstance(text, unicode_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.encode("utf-8")


def to_unicode(text):
    """
        Converts a string argument to a unicode string.

        If the argument is already a unicode string or None, it is returned
        unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(text, _TO_UNICODE_TYPES):
        return text
    assert isinstance(text, bytes_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.decode("utf-8", 'ignore')


channel_re = re.compile(r'[a-z0-9]')
phone_re = re.compile(r'[0-9]{11}')


def is_valid_channel_name(channel):
    return channel_re.match(channel)


def is_valid_phone(phone):
    return phone_re.match(phone)


def gen_order_no():
    return uuid.uuid4()


def get_random_str(num=15):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))


def fill_zero(data, max_length=10):
    data = str(int(data))
    zero_num = max_length - len(data)
    if zero_num >= 1:
        return '0' * zero_num + str(data)
    return data


def replace_html_tag(content):
    return re.sub('<[^>]*?>', '', content)


def remove_emoj(text):
    text = to_unicode(text)
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
    filtered_string = re_pattern.sub(u'', text)
    return filtered_string


def url_encode_dict(target_dict):
    encode_list = []
    for k, v in target_dict.items():
        if not isinstance(v, (str, unicode)):
            v = str(v)
        encode_list.append('{}={}'.format(k, urllib.quote(v)))
    return '&'.join(encode_list)


def safe_int(value, default=0):
    try:
        value = int(value)
    except:
        value = default
    return value


class FancyDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k


def ip_to_ip_num(ip):
    """
    ip转换为ip对应的数字，例如
    '101.226.103.0/25' -> 1709336320
    :param ip:
    :return:
    """
    return int(socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0]))


def ip_num_to_ip(ip_num):
    """
    ip对应的数字转换为ip
    1709336320 -> '101.226.103.0/25'
    :param ip_num:
    :return:
    """
    return socket.inet_ntoa(struct.pack('I', socket.htonl(ip_num)))


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        if isinstance(obj, set):
            return list(obj)
        return super(JsonEncoder, self).default(obj)


def mask_name(raw_name):
    """
    给名字打"*"
    :param raw_name:
    :return:
    """
    if not raw_name:
        return ''

    name = raw_name[0] + '*' * (len(raw_name) - 1)
    return name


def mask_phone(raw_phone):
    """
    给名字打"*"
    :param raw_phone:
    :return:
    """
    if not raw_phone:
        return ''
    try:
        length = len(raw_phone)
        raw_phone = raw_phone[0:3] + '*' * (len(raw_phone) - 7) + raw_phone[length - 4:length]
        return raw_phone
    except Exception, e:
        logging.error(e)
        return raw_phone


def mask_id_no(raw_id_no):
    """
    给名字打"*"
    :param raw_id_no:
    :return:
    """
    if not raw_id_no:
        return ''
    try:
        length = len(raw_id_no)
        raw_id_no = raw_id_no[0:3] + '*' * (length - 7) + raw_id_no[length - 4:length]
        return raw_id_no
    except Exception, e:
        logging.error(e)
        return raw_id_no


def send_email(receiver, title, body):
    host = 'smtp.mxhichina.com'
    sender = 'report@heiniubao.com'
    pwd = 'Heiniu1003'
    msg = MIMEText(body, 'html', 'utf-8')
    msg['subject'] = title
    msg['from'] = sender
    if isinstance(receiver, list):
        msg['to'] = ",".join(receiver)
        # print msg
    else:
        msg['to'] = receiver
        # print msg
    s = smtplib.SMTP(host, port=80)
    # s.starttls()
    s.login(sender, pwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    s.close()


def add_extension_url_arg(url, name, value):
    if '?' in url:
        separator = '&'
    else:
        separator = '?'
    try:
        value_quote = urllib.quote(value)
    except:
        value_quote = ''
    url = '{url}{separator}{name}={value}'.format(
        url=url, separator=separator, name=name, value=value_quote
    )
    return url


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
           
