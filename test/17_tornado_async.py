# coding:utf-8
from tornado.web import Application, RequestHandler, asynchronous
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return, Task
import tornado.gen
import json
import time
"""
异步：为了防止cpu密集型或者io密集操作，影响别的客户端访问，引入协程异步（tornado单进程）
        1.在需要异步执行的方法加入coroutine装饰器
        2.在调用函数中使用yield Task(self.fun, (params))获取返回值
"""


define(name="port", default=8000, type=int)
define(name="conf", default=dict(), type=dict)


class IndexHandler(RequestHandler):

    @asynchronous # 不关闭连接，也不发送响应
    def get(self, *args, **kwargs):
        http = AsyncHTTPClient()
        """回调异步，fetch返回给回调函数参数(self,code: HTTP状态码，如 200 或 404 reason: 状态码描述信息
                                  # body: 响应体字符串
                                  # error: 异常（可有可无）)"""
        http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=183.128.116.112",
                   callback=self.basefinish)

    def basefinish(self, data):
        if data:
            json_data = json.loads(data.body)
            self.write(json_data["city"])
            self.finish()
        else:
            self.send_error(404)
        # self.on_finish()


class GetHandler(RequestHandler):
    @coroutine
    def get(self, *args, **kwargs):
        result = yield Task(self.io_long)
        self.write(result)
    @coroutine
    def io_long(self):
        time.sleep(10)
        return u'异步完成'

class TestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("ok")


if __name__ == "__main__":
    options.parse_config_file("./config.py")
    app = Application([
        (r'/', IndexHandler),
        (r'/a/', GetHandler),
        (r'/b/', TestHandler)
    ], **options.conf)
    cur_server = HTTPServer(app)
    cur_server.listen(options.port)
    IOLoop.current().start()