
import tornado.gen
import tornado.httpclient
import json

@tornado.gen.coroutine
def get_short_url(phone):
    print phone
    url = 'https://www.heiniubao.com/'
    request_url = 'http://suo.im/api.php?format=json&url={}'.format(url)
    try_times = 0
    max_times = 5
    result = '', 'ERROR'
    while try_times < max_times:
        try_times += 1
        response = yield tornado.httpclient.AsyncHTTPClient().fetch(request_url)
        if response:
            response = json.loads(response.body)
            print response
            short_url = response.get('url', '')
            error_msg = response.get('err', '')
            result = short_url, error_msg
            if short_url:
                raise tornado.gen.Return(result)
    raise tornado.gen.Return(result)



if __name__ == "__main__": 
    phone='13691036309'
    tornado.ioloop.IOLoop.current().run_sync(lambda: get_short_url(phone))
#     get_short_url(phone)