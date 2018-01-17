# coding:utf-8
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado.httpserver import HTTPServer
import json

"""
1.self.set_header(key,value):设置报文头
2.set_default_headers():可以重写该方法来封装报文头，该方法会在http处理方法前被调用，如果在http处理方法中使用set_header()可覆盖该方法中的同名头
3.set_status(status_code, reason=None):设置状态码，如果reason为none则状态码必须为标准状态而不是自定义,注意：状态码为int类型
4.self.redirect(url):重定向
5.self.send_error(status_code,content):发送错误，默认的content是没有效果的，需要重写write_error()函数，该函数执行后缓冲流就finish了，不能在write
6.write_error(status_code,**kwargs):重写该函数，自定义错误体，该函数会处理send_error,注意code值必须为标准值
"""

define(name="port", default=8001, type=int, help="Bind Port")


class RequestTest(RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.write("%d,reason: %s" % (status_code, kwargs["content"]))

    def get(self, *args, **kwargs):
        self.write("123")
        li = {"name": "xiaomi", "age": 12, "sex": "男".decode("utf-8")}
        # self.set_header("Charset", "utf-8")
        # self.write(json.dumps(li))
        # write可输出内容到缓存流即http的body，函数可执行多次write，直到调用self.finish()函数，统一发送
        # 输出json，如果不手动转json则tornado会自动转，但是改变header的信息
        self.write(li)
        # self.set_status(status_code=404)
        self.send_error(status_code=404, content="错误msg")


if __name__ == "__main__":
    options.parse_command_line()
    app = Application([
        (r'/', RequestTest)
    ], debug=True)
    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()