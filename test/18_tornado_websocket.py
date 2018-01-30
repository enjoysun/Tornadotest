# coding:utf-8
from tornado.web import RequestHandler, Application
from tornado.options import options, define
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.websocket import WebSocketHandler

"""
WEBSOCKET:
        1.需要导入tornado.webscoket的websockethandler模块
        2.该模块提供了：
                    1.open：前端ws协议即客户端链接上时的函数（需要重写）
                    2.on_message：发送数据给客户端函数（需重写）
                    3.on_close:websocket链接协议被关闭后操作函数（需重写）
                    4.write():写入数据到缓冲流，由on_message函数调用后发送到客户端
"""


define(name="port", default=8000, type=int, help="Port Bind")
define(name="conf", default=[], type=dict, help="Conf Bind")


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render("chat.html")


class ChatHandler(WebSocketHandler):

    users = []

    def open(self, *args, **kwargs):
        for user in self.users:
            user.write_message("%s上线了" % self.request.remote_ip)
        self.users.append(self)

    def on_message(self, message):
        for user in self.users:
            user.write_message("%s:%s" % (self.request.remote_ip, message))

    def on_close(self):
        self.users.remove(self)
        for user in self.users:
            user.write_message("%s下线了" % self.request.remote_ip)


if __name__ == "__main__":
    options.parse_config_file("./config.py")
    app = Application([
        (r'/', IndexHandler),
        (r'/chat', ChatHandler),
    ], **options.conf)
    cyr_server = HTTPServer(app)
    cyr_server.listen(options.port)
    IOLoop.current().start()