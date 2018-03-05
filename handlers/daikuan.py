#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base.sys_handler
import tornado.gen
import logging

import base.func_helper
class DaikuanHandler(base.sys_handler.BasePageHandler):
    
    def initialize(self):
        super(DaikuanHandler, self).initialize()
        self.page_param['title']='测试页面'
        self.page_param['keywords']='测试页面'
        self.page_param['description']='测试页面'

    @tornado.gen.coroutine
    @base.func_helper.authenticated
    def get(self):
#         self.session.set('name','wangxiaofei')
#         print self.session.get('name')
        logger = logging.getLogger()
        logger.info('test')
        kwargs={}
        kwargs['page_param']=self.page_param
        self.render('heiniu_loan3/wap_home2.html',**kwargs)
        
        
        
        
class LoginHandler(base.sys_handler.BasePageHandler):
    
    def initialize(self):
        super(LoginHandler, self).initialize()
        self.page_param['title']='登录测试页面'
        self.page_param['keywords']='登录测试页面'
        self.page_param['description']='登录测试页面'

    @tornado.gen.coroutine
    def get(self):
        kwargs={}
        kwargs['page_param']=self.page_param
        self.render('heiniu_loan3/wap_login.html',**kwargs)