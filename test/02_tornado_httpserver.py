# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver

"""自定义服务器绑定"""
class Indexhandler(tornado.web.RequestHandler):

    def get(self):
        self.write("hello word")


if __name__ == "__main__":
    app = tornado.web.Application([(r'/', Indexhandler)])
    server_self = tornado.httpserver.HTTPServer(app)
    # 单进程绑定写法
    # server_self.listen(8000)
    # 多进程写法
    server_self.bind(8000)
    # num为0或者none默认开启cup核数同等线程，如果指定大于1则开启num线程数量
    server_self.start(0)
    tornado.ioloop.IOLoop.current().start()
