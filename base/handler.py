#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import base.regex
import pycket.session

class BasePageHandler(tornado.web.RequestHandler):
    def initialize(self):
        super(BasePageHandler, self).initialize()
        self.is_wap = 0
        self.is_ios = False
        self._check_is_wap()
        self.http_referer = self.request.headers.get('Referer', '')
        self.remote_ip = self.request.remote_ip
        self.uri = self.request.uri
        self.user_agent = self.request.headers.get('user-agent', '')
        self.session = pycket.session.SessionManager(self)
        
        
        
        
        
    
        
    def _check_is_wap(self):
        user_agent = self.request.headers.get('user-agent', '')
        if user_agent != '' and base.regex.re_user_agent.search(user_agent):
            self.is_wap = 1
            if self.re_ios_user_agent.search(user_agent):
                self.is_ios = True
                
                
    def _get_request_domain(self):
        hostport = self.request.host.split(":")
        if len(hostport) == 2:
            host = hostport[0]
            port = int(hostport[1])
        else:
            host = self.request.host
            port = 443 if self.request.protocol == "https" else 80
        return host,port