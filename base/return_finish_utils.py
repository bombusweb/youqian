# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

import json



class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
    
    @tornado.gen.coroutine 
    def get(self):
        ajax_dict = {'status': 1,'msg':u'系统异常！'}
        ajax_str = json.dumps(ajax_dict)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(ajax_str)
        self.finish()
        print 'after return '
      
    @tornado.gen.coroutine 
    def post(self):
        ajax_dict = {'status': 1,'msg':u'系统异常！'}
        ajax_str = json.dumps(ajax_dict)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(ajax_str)
        return
        print 'after return '
        
def make_app():
    return tornado.web.Application([
        (r"/",MainHandler),
        ])

if __name__=="__main__":
    
    app = make_app()
    HTTP_SERVER = tornado.httpserver.HTTPServer(app, xheaders=True)
    HTTP_SERVER.listen(8080)
    tornado.ioloop.IOLoop.current().start()