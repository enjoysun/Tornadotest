# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

define(name="name", default="小米", type=str, help="sayyou")
define(name="port", default=None, type=int, help="")
define(name="subject", default=[], type=str, multiple=True)


class IndexPageHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.write("hello {0},port={1},sub={2}".format(options.name, options.port, options.subject))


if __name__ == "__main__":
    options.parse_config_file(r'./config.py')
    options.parse_command_line()
    app = tornado.web.Application([(r'/', IndexPageHandler)])
    cur_server = tornado.httpserver.HTTPServer(app)
    cur_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()



