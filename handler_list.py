#!/usr/bin/env python
# -*- coding: utf-8 -*-

import handlers.daikuan

system_handler_list=[
    (r"/daikuan", handlers.daikuan.DaikuanHandler),
    (r"/login", handlers.daikuan.LoginHandler),
    ]