# coding:utf-8
from tornado.web import Application, RequestHandler, url
from tornado.options import options, define
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
"""
本章练习错误点：initialize（）接收参数函数，注：只接受querystring传值post不适用
介绍request类作用：
method HTTP的请求方式，如GET或POST;
host 被请求的主机名；
uri 请求的完整资源标示，包括路径和查询字符串；
path 请求的路径部分；
query 请求的查询字符串部分；
version 使用的HTTP版本；
headers 请求的协议头，是类字典型的对象，支持关键字索引的方式获取特定协议头信息，例如：request.headers["Content-Type"]
body 请求体数据；
remote_ip 客户端的IP地址；
files 用户上传的文件，为字典类型，型如：
"""

define(name="port", default=8000, type=int, help="Bind Port")


class Upload_Handler(RequestHandler):

    def get(self, *args, **kwargs):
        self.write("hello")

    def post(self, *args, **kwargs):
        self.write(self.get_argument("acc"))
        self.write("<br />")
        self.write(self.get_argument("pss"))
        self.write("<br />")
        self.write(self.request.method)
        self.write("<br />")
        self.write(self.request.host)
        self.write("<br />")
        self.write(self.request.uri)
        self.write("<br />")
        self.write(self.request.path)
        self.write("<br />")
        self.write(self.request.version)
        self.write("<br />")
        self.write(str(self.request.files.get("uploadfile")))

        # self.write(str(self.request.headers))
        # self.write("<br />")
        # self.write(self.request.body)
        # self.write("<br />")
        # self.write(self.request.remote_ip)
        if self.request.files.get("uploadfile"):
            file = open("./img/test.jpg", 'w+')
            file.write(self.request.files.get("uploadfile")[0]["body"])
            file.close()


if __name__ == "__main__":
    options.parse_command_line()
    app = Application([
        (r'/welcome/', Upload_Handler),
    ], debug=True)
    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()