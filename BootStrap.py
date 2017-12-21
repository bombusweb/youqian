#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from base.loggers import SystemLogger

class DefaultErrorHandler(tornado.web.RequestHandler):
    """Generates an error response with ``status_code`` for all requests."""

    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

    def write_error(self, status_code, **kwargs):
        error_msg = str(status_code) + ' 抱歉！页面出错'
        self.render('wap/wap_error.html', error_msg=error_msg)

tornado.web.ErrorHandler = DefaultErrorHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", None),
            (r"/intro.html", 'None'),
        ]
        
        

def main():
    print 'hello world'

if __name__ == "__main__":
    main()
