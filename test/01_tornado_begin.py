# coding:utf-8

import tornado.web
import tornado.ioloop


class Indexhanler(tornado.web.RequestHandler):
    """首页处理类"""
    def get(self):
        self.write("hello tornado")


if __name__ == "__main__":
    app = tornado.web.Application([(r"/", Indexhanler)])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
