#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import signal
import time  

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.write('begin init!') 
        self.write('\t\n')
    def get(self):
        self.set_header('name', 'value')
        self.write("hello world!")
        self.write('\n')
def make_app():
    return tornado.web.Application([
        (r"/",MainHandler),
        ])

def signal_handler():
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    global server
    print 'before stop'
    server.stop()

    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 5
    print 'deadline:%s' % deadline
    
    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
            print 'add_timeout' 
        else:
            io_loop.stop()

    stop_loop()
    make_app().destroy()

if __name__=="__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    app=make_app()
#     app.listen(8001,'127.0.0.1')
    global server
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(8001)
    
    tornado.ioloop.IOLoop.current().start()