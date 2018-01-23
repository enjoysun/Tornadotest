# coding=utf-8
from tornado.web import Application, RequestHandler
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import time
"""
1.time和datetime模块区别：time趋向与系统的操作，datetime是对time的进一步封装
2.time下的strftime和strptime：strftime:时间转为字符串  strptime:字符串转为时间 mktime:转为当前地区的utc时间
3.set_cookie(name, value, domain:域名, path：匹配的请求路径, expires:过期时间, expires_days:过期时间（天数）)
4.set_secure_cookie：1.要在Application中设置cookie_secret="t8S2e3I9SD6h5bVvYLLQOepXBoqgcECuqcMxKtEHyzA="加密的签名根据自己需求设置
"""

define(name="port", default=8000, type=int, help="BIND PORT")
define(name="conf", default=[], type=dict, help="File Msg")


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # self.set_cookie("aa", "bb", expires=time.mktime(time.strptime("2018-1-23 22:46", "%Y-%m-%d %H:%M"))) #不带签名设置cookie
        self.set_secure_cookie("ff", "gg", expires=time.mktime(time.strptime("2018-1-23 23:46", "%Y-%m-%d %H:%M")))
        self.write(str(self.get_secure_cookie("ff")))


if __name__ == "__main__":
    options.parse_config_file("./config.py")
    app = Application([
        (r'/', IndexHandler),
    ], **options.conf)
    current_server = HTTPServer(app)
    current_server.listen(options.port)
    IOLoop.current().start()