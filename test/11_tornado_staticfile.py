# coding:utf-8
from tornado.web import Application, url, RequestHandler
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import os
"""
注意：1.static_path 的挂载路径是 /static
     2.要设置static_path来指向实际静态文件目录
     3.os和sys区别：os是操作机器系统的模块，sys是操作解释器的模块
"""

define(name="port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.write("<a href='/static/html/test.html'>静态文件链接测试</a>")


if __name__ == "__main__":
    app = Application([
        (r'/', IndexHandler),
    ], debug=True, static_path=os.path.join(os.path.dirname(__file__), "staticfiles"))
    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()