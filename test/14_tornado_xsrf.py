# coding:utf-8
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import os
"""
xsrf防跨站攻击：
1.在application类中传入字典 xsrf_cookies=True 开启xsrf
2.开启后tornado会产生xsrf_token来验证是否为同一操作者提交操作,该token会被写入http头的cookie,返回给服务端验证分两种情况：
        1.使用模板来执行post,该方法只需在提交表单中加入{%module xsrf_form_html()%}标签即可完成验证（产生一个隐藏的input),tornado会自行验证
        2.前后端分离不使用模板分为两种情况：
            A：使用form表单提交：
            B：使用ajax提交：
"""

define(name="port", default=8000, type=int)
define(name="conf", default={}, type=dict)


class BaseFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(BaseFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token

    def post(self, *args, **kwargs):
        self.write(self.get_argument("uname"))


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        # self.set_secure_cookie("aa", "bb")
        # self.write("ok")
        # 1.xsrf防跨站在模板中使用
        self.render("xsrftest.html")

    def post(self, *args, **kwargs):
        self.write(self.get_argument("uname"))


if __name__ == "__main__":
    options.parse_config_file("./config.py")
    app = Application([
        (r'/', IndexHandler),
        (r'/form/(.*)', StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "statics/html")))
    ], xsrf_cookies=True, **options.conf)
    cur_server = HTTPServer(app)
    app.listen(options.port)
    IOLoop.current().start()