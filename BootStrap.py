#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.options 
import tornado.httpserver
import base.sys_config
import os
import time
import handler_list

import signal


from base.loggers import SystemLogger


tornado.options.define("port", default=8080, help="run on the given port", type=int)
tornado.options.define("is_worker", default=0, help="run as the worker", type=int)
tornado.options.define("unit_test", default=0, help="run as the unit tester", type=int)

APPLICATION = None
HTTP_SERVER = None

class DefaultErrorHandler(tornado.web.RequestHandler):
    """Generates an error response with ``status_code`` for all requests."""

    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

    def write_error(self, status_code, **kwargs):
        error_msg = str(status_code) + u' 抱歉！页面出错'
        self.render('wap/wap_error.html', error_msg=error_msg)

tornado.web.ErrorHandler = DefaultErrorHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = handler_list.system_handler_list
        sys_config=base.sys_config.SystemConfig.instance()
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=False,
            xsrf_cookies=False,
            cookie_secret="xFllasd120i0safsa;dfk.,';@%^&!)--=",
            login_url="/login",
            pycket={
                'engine': sys_config.pycket.get('engine'),
                'storage': {
                    'host': sys_config.pycket.get('storage_host'),
                    'port': int(sys_config.pycket.get('storage_port')),
                    'password': sys_config.pycket.get('storage_password'),
                    'db_sessions': int(sys_config.pycket.get('storage_db_sessions')),
                    'db_notifications': int(sys_config.pycket.get('storage_db_notifications')),
                    'max_connections': int(sys_config.pycket.get('storage_max_connections')),
                },
                'cookies': {
                    'expires_days': int(sys_config.pycket.get('cookies_expires_days')),
                    'expires': int(sys_config.pycket.get('cookies_expires')),
                    'domain': sys_config.pycket.get('domain'),
                },
            
            },
            autoreload=True,
        )
        super(Application, self).__init__(handlers, **settings)
        
        self.shutdown_listener = []
        
        
        
    def destroy(self):
        for listener in self.shutdown_listener:
            listener.destroy()
        
        
    def register_shutdown_listeners(self, listener):
        self.shutdown_listener.append(listener)
        
        
def signal_handler():
    tornado.ioloop.IOLoop.instance().add_callback(shutdown) 
    
def shutdown():
    global APPLICATION
    global HTTP_SERVER
    # 不接收新的 HTTP 请求
    HTTP_SERVER.stop()

    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 5

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            io_loop.stop()

    stop_loop()
    APPLICATION.destroy()     
        
        
        

def main():
    global APPLICATION
    global HTTP_SERVER

    tornado.options.parse_command_line()
    APPLICATION = Application()
    HTTP_SERVER = tornado.httpserver.HTTPServer(APPLICATION, xheaders=True)
    HTTP_SERVER.listen(tornado.options.options.port)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()

if __name__ == "__main__":
    main()