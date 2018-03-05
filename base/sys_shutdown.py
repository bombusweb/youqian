#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

try:
    sys.modules['json'] = __import__('ujson')
except ImportError:
    pass

import os
import time
# os.environ["TZ"] = "Asia/Shanghai"
# time.tzset()

import logging
import time
import signal

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

__author__ = 'weizs'

# simple grace shutdown app.py with tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret='ssaaswq',
            autoescape=None,
            login_url='/oauth/sign-in',
            # debug=True,
        )

        handlers = [
            (r"/", MainHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    server.stop()

    logging.info('Will shutdown in %s seconds ...', 10)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 10

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()


def main():
    try:
        port = int(sys.argv[1])
    except:
        port = 15003

    global server

    server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    server.listen(port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop.instance().start()

    logging.info("Exit...")

if __name__ == "__main__":
    main()