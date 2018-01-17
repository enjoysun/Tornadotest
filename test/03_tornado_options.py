# coding:utf-8
"""tornado.options模块：全局参数定义，转换和存储"""

import tornado.web
import tornado.httpserver
import tornado.ioloop
import os
# 导入全局参数模块
import tornado.options
# 定义全局变量:name=全局变量名 default=默认值 type=变量类型 help=帮助说明 multiple=是否为列表即多个值
tornado.options.define(name="port", default=8000, type=int, help="端口设置参数")
tornado.options.define(name="subject", default=['c++', 'c#'], type=str, multiple=True, help="科目")

class IndexHandler(tornado.web.RequestHandler):

    """案首页处理"""

    def get(self, *args, **kwargs):
        self.write("hello {0}".format(tornado.options.options.subject))


if __name__ == "__main__":
    # 转换命令行参数，并将转换后的值对应的设置到全局options对象相关属性上。追加命令行参数的方式是 --myoption=myvalue
    # tornado.options.parse_command_line()
    # 加载配置文件变量(注意配置文件就是.py的文件,路径注意)
    tornado.options.parse_config_file('./config/port_setting.py')
    print tornado.options.options.subject
    app = tornado.web.Application([(r'/', IndexHandler)])
    server_cur = tornado.httpserver.HTTPServer(app)
    server_cur.bind(tornado.options.options.port)
    server_cur.start(1)
    tornado.ioloop.IOLoop.current().start()