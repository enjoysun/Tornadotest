# coding:utf-8
from tornado.web import Application, url, RequestHandler, StaticFileHandler
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import os
"""
注意：1.static_path 的挂载路径是 /static,可以通过static_url_prefix修改默认的挂载路径
     2.要设置static_path来指向实际静态文件目录
     3.os和sys区别：os是操作机器系统的模块，sys是操作解释器的模块
     4.StaticFileHandler:自由映射静态文件与其访问路径url的模块，该类接收两个参数（path：映射的静态文件路径，default_filename:默认访问文件）
模板：
    1.render是渲染模板页面的函数接收两个参数（模板页面名称，渲染字典参数）
    2.模板语法:{{}}和django类似，可接受变量，也可以执行表达式
    3.支持控制流程语句但是要有结尾如{% if %}{% else %}{% end %}
    4.Tornado模板模块提供了一个叫作static_url的函数来生成静态文件目录下文件的URL,(注意：static_url（）搜寻开始目录是挂载目录即static)。
"""

define(name="port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        rootmsg = dict(price=155, description="哈哈", score="18", comments="没有", p1=1.1, p2=2.2, sm="姜嘉豪的小屋")
        self.write("<a href='/static/html/index.html'>静态文件链接测试</a>")
        self.render("index.html", **rootmsg)


class TestHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render("new.html", sm="")

    def post(self, *args, **kwargs):
        sm = self.get_argument("txt")
        self.render("new.html", sm=sm)


if __name__ == "__main__":
    app = Application([
        (r'/', IndexHandler),
        (r'/test/', TestHandler),
        (r'/app/(.*)', StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "statics/html")})
    ],
        debug=True,
        static_path=os.path.join(os.path.dirname(__file__), "statics"),  # 静态文件路径配置
        template_path=os.path.join(os.path.dirname(__file__), "templates"),  # 模板路径配置
    )
    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()