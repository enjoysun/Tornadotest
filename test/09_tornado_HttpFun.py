# coding=utf-8
from tornado.web import Application, url, RequestHandler
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import re
"""
HTTP方法
       1.initialize():对应每个请求的处理类Handler在构造一个实例后首先执行initialize()方法。路由映射中的第三个字典型参数的键值会作为该方法的命名参数传递
       2.prepare():不论以何种HTTP方式请求，都会执行prepare()方法
"""

define(name="port", default=8000, type=int, help="Bind Port")


class IndexHandler(RequestHandler):

    def initialize(self, age=13):
        self.age = age

    def get(self, *args, **kwargs):
        self.write(self.get_argument("age"))

    def prepare(self):
        str_url = str(self.request.uri)
        self.write(re.search(r'^=\d+', str_url).group(0))


class PostHandler(RequestHandler):

    def post(self, *args, **kwargs):
        self.write(self.get_argument("name"))


if __name__ == "__main__":
    options.parse_command_line()
    app = Application([
        (r'/', IndexHandler),
        url(r'/wel/', PostHandler, name="welurl")
    ], debug=True)
    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()