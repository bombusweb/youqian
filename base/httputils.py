# -*- coding: utf-8 -*-

import tornado.httpclient
import tornado.gen
import datetime
import logging

@tornado.gen.coroutine
def async_http_fetch(url, timeout=5, post_body=None, method='GET', headers=None, validate_cert=None):
    http_request = tornado.httpclient.HTTPRequest(
        url=url,
        method=method,
        body=post_body,
        connect_timeout=timeout,
        request_timeout=timeout,
        headers=headers,
        validate_cert=validate_cert
    )

    http_client = tornado.httpclient.AsyncHTTPClient()

    response = ''
    begin_time = datetime.datetime.now()
    http_response = None
    try:
        http_response = yield http_client.fetch(http_request)
        response = http_response.body
    except Exception as e:
        logging.error(e)
    finally:
        cost_time = (datetime.datetime.now() - begin_time).total_seconds()
        if http_response and 'Content-Type' in http_response.headers and http_response.headers['Content-Type'] == 'image/png':
            logging.info('{}####{}####{}'.format(url, post_body, cost_time))
        else:
            logging.info('{}####{}####{}####{}'.format(url, post_body, response, cost_time))


    raise tornado.gen.Return(response)


@tornado.gen.coroutine
def async_http_fetch_response(url, timeout=5, post_body=None, method='GET', headers=None):
    http_request = tornado.httpclient.HTTPRequest(
        url=url,
        method=method,
        body=post_body,
        connect_timeout=timeout,
        request_timeout=timeout,
        headers=headers
    )

    http_client = tornado.httpclient.AsyncHTTPClient()

    begin_time = datetime.datetime.now()
    http_response = None
    response_body = ''
    try:
        http_response = yield http_client.fetch(http_request)
        response_body = http_response.body
    except Exception as e:
        logging.error(e)
    finally:
        cost_time = (datetime.datetime.now() - begin_time).total_seconds()
        if http_response and 'Content-Type' in http_response.headers and http_response.headers['Content-Type'] == 'image/png':
            logging.info('{}####{}####{}'.format(url, post_body, cost_time))
        else:
            logging.info('{}####{}####{}####{}'.format(url, post_body, response_body, cost_time))


    raise tornado.gen.Return(http_response)