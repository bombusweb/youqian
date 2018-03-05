# -*- coding: utf-8 -*-

import functools
import urlparse
from urllib import urlencode
from tornado.web import HTTPError

def authenticated(method):
    
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_current_wx_oauth_user():
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper