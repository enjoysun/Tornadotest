# coding:utf-8

from tornado.web import RequestHandler, Application, url
from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado.httpserver import HTTPServer

define(name="port", default=8000, type=int, help="端口")


class Test(RequestHandler):
    def get(self, *args, **kwargs):
        python_url = self.reverse_url("person")
        self.write('<a href="%s">itcast</a>' % python_url)


class IndexHandler(RequestHandler):
    """application详解"""
    def initialize(self, name, age):
        self.name = name
        self.age = age

    def get(self, *args, **kwargs):
        cpp_url = self.reverse_url("person")
        self.write(cpp_url)


class Myhandler(RequestHandler):

    def initialize(self, subject, sex):
        self.sort = subject
        self.sex = sex

    def get(self, *args, **kwargs):
        self.write("I like {0},i am {1}".format(self.sort, self.sex))


if __name__ == "__main__":
    """
    Application类设置参数：
    1.Application([],debug=True):debug为True时tornado工作在调试环境，默认为false工作在生产模式
    2.Application([路由列表],debug=False)：
                  1.路由列表为元组即(路由路径，处理类，{参数})，参数为字典，在处理类的initialie方法中接收，接收方式以键名为参数传递，那属性接收，可设置多个
                  2.路由设置name属性则不能用元组，用tornado.web.url的url函数来接收如url(路由路径，处理类，{参数}，name=路由名称),取值时使用RequestHandler.reverse_url(name)来获取该名子对应的url
    
    """
    app = Application([
        (r'/', IndexHandler),
        (r'/test', Test),
        (r'/my', Myhandler, {"subject": "python", "sex": "男"}),
        url(r'/app', IndexHandler, {"name": "小王", "age": "12"}, name="person"),
        ],
        debug=True)

    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()