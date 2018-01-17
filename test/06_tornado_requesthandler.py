# coding:utf-8
from tornado.web import RequestHandler, url, Application
from tornado.options import options, define
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
define(name="port", default=8000, type=int, help="binding port")


"""
本章练习RequestHandler类：
一.RequestHandler类是用来接收和返回请求的类
二.对于querystring类型的参数接收：
           1.get_query_argument(name="", default="", strip=bool)
           从请求体和查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值，如果不存在则抛出异常
           name请求体的name也就是key值,default设置默认值，strip去除左右的空字符串
           2.get_query_arguments(name="", default="", strip=bool)
           参数与上一致，但是可以接收多个同名参数返回一个列表，如果一个没有则返回空列表，如：http://127.0.0.1:8001/welcome/?sex=1&sex=2
三.对于获取请求体参数接收：
           1.get_body_argument(name="", default="", strip=bool)
           get_body_argument用于接收post参数
           2.get_body_arguments使用方法同上
四.对于获取报文头和其他信息可以使用RequestHandler,request来获取信息
    
"""

class TestHandler(RequestHandler):
    """index"""
    def get(self, *args, **kwargs):
        self.write("<a href='{0}'>点击登录</a>".format(self.reverse_url("wel")))
        # self.write("<a href='../htmltest/RequestHandler.html'>输入</a>")


class HelloHandler(RequestHandler):
    def initialize(self, name, age):
        self.name = name
        self.age = age

    def get(self, *args, **kwargs):
        self.write("接收单个query参数：{0}".format(self.get_query_argument("sex", strip=True)))
        self.write("</ br>")
        self.write("</ hr>")
        self.write("接收多个query参数：{0}".format(self.get_query_arguments("sex", strip=True)))
        self.write("</ br>")
        self.write("</ hr>")
        self.write("hello i am {0} and {1} old".format(self.name, self.age))

    def post(self, *args, **kwargs):
        self.write("接收单个body参数：账号：{0},密码:{1}".format(self.get_body_argument("acc"), self.get_body_argument("pass")))


if __name__ == "__main__":
    options.parse_command_line()
    app = Application([
        (r'/', TestHandler),
        # (r'/msg', MsgHandler, {"name": "xiaomi", "age": "12"}),
        url(r'/welcome/', HelloHandler, {"name": "xiaomi", "age": "12"}, name="wel")
    ], debug=True)
    cur_app = HTTPServer(app)
    cur_app.listen(options.port)
    IOLoop.current().start()