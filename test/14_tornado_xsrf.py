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
            A：使用form表单提交：需要在form表单中生成隐藏的input，将cookie中的_xsrf键名的cookie截取出来后值传递给input的value，提交后
                tornado会自动接收（input的name必须为_xsrf），详情见html下的xseftest_form.html文件
            B：使用ajax提交：ajax提交post分为两种情况：
                a：提交数据格式为键值对：需要在键值对数据中添加_xsrf=xsrf_token,xsrf_token同上截取
                b:提交数据格式为json:需要在ajax请求体中添加header:{"X-XSRFToken":xsrf_token}
"""

define(name="port", default=8000, type=int)
define(name="conf", default={}, type=dict)


class BaseFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(BaseFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        # self.set_secure_cookie("aa", "bb")
        # self.write("ok")
        # 1.xsrf防跨站在模板中使用
        self.render("xsrftest.html")

    def post(self, *args, **kwargs):
        print self.get_argument("uname")
        self.write(self.get_argument("uname"))


class AjaxHandler(RequestHandler):
    def post(self, *args, **kwargs):
        uname = self.get_argument("uname")
        self.write(uname)


if __name__ == "__main__":
    options.parse_config_file("./config.py")
    app = Application([
        (r'/', IndexHandler),
        (r'/form/(.*)', StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "statics/html"))),
        (r'/new', AjaxHandler),
    ], xsrf_cookies=True, **options.conf)
    cur_server = HTTPServer(app)
    app.listen(options.port)
    IOLoop.current().start()