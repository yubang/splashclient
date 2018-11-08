# coding: UTF-8


"""
基于requests来操作splash
@author: yubang
创建于2018年11月8日
"""

from json import dumps
from copy import copy
from base64 import b64encode, b64decode
import requests


class SplashException:
    class SplashServerError(Exception):
        def __init__(self):
            super().__init__("Splash服务端异常")

    class SplashAPIError(Exception):
        def __init__(self):
            super().__init__("Splash调用异常")


class SplashArgs:
    class HTTP_METHOD:
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'


class SplashClient:
    def __init__(self, splash_url, default_time=30, default_proxy=None, default_header=None, default_wait=1):
        """
        初始化Splash客户端
        :param splash_url: splash服务端地址
        :param default_time: 默认超时时间
        :param default_proxy: 默认代理，None不使用代理，{"protocol": "http", "ip": "IP地址", "port": 端口}
        :param default_header: 需要附加的header
        """
        self.splash_url = splash_url + "/execute"
        self.default_time = default_time
        self.default_proxy = default_proxy
        self.default_header = default_header if default_header else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
        }
        self.default_wait = default_wait

    def request_splash(self, url, http_method, timeout, wait, need_png=False):
        """请求接口"""

        headers = copy(self.default_header)

        if need_png:
            png = "png = splash:png(),"
        else:
            png = ""

        lua_source = """
                    function main(splash, args)
                      splash:go(args.url)
                      splash:wait(%(wait).2f)
                      splash:set_user_agent("%(ua)s")
                      return {
                        %(png)s
                        html = splash:html()
                      }
                    end
        """ % {
            "wait": wait,
            "ua": headers.get("User-Agent", ""),
            "png": png
        }

        source = {
            "url": url,
            "http_method": http_method,
            "timeout": timeout,
            "wait": wait,
            "lua_source": lua_source,
            "har": 1,
            "html": 1,
            "html5_media": False,
            "images": 0,
            "load_args": {},
            "png": 1,
            "render_all": False,
            "resource_timeout": 0,
            "response_body": False,
            "save_args": [],
            "viewport": "1024x768"
        }

        if self.default_proxy:
            source['proxy'] = "%s://%s:%d" % (
                self.default_proxy['protocol'],
                self.default_proxy['ip'],
                self.default_proxy['port'],
            )
        source['headers'] = headers
        data = dumps(source)
        try:
            result = requests.post(self.splash_url, data=data, headers={"Content-Type": "application/json"},
                                   timeout=timeout)
        except:
            raise SplashException.SplashServerError()

        if result.status_code != 200:
            raise SplashException.SplashAPIError()

        return result.json()

    def render(self, url, http_method=SplashArgs.HTTP_METHOD.GET):
        """"
        获取渲染后的页面
        :param url: 目标网页地址
        :param http_method: 请求方式，GET, POST, PUT, DELETE
        """
        result = self.request_splash(url, http_method, self.default_time, self.default_wait)
        return result['html']

    def png(self, url, http_method=SplashArgs.HTTP_METHOD.GET, base64=False):
        """获取网页截图"""
        result = self.request_splash(url, http_method, self.default_time, self.default_wait, need_png=True)
        data = result['png']
        if not base64:
            return b64decode(data)

