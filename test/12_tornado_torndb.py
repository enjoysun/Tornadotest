# coding:utf-8
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.options import options, define
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import torndb

"""
封装版本的数据库访问。
   1.安装mysql：mysql-service,mysql-client,libmysqlclient-dev
   2.static_url函数只用于模板页面
   3.执行sql：execute返回最后一条记录id   execute_rowcount:返回执行成功行数
   4.查询sql: get返回一条数据torndb.row类型  query:返回tornado.row集合查询多条数据
"""

define(name="port", default=8000, type=int, help="BIND PORT")
define(name="conf", default=dict(), type=dict, help="File path")


class BaseApplication(Application):

    def __init__(self, *args, **kwargs):
        super(BaseApplication, self).__init__(*args, **kwargs)
        condic = dict(host="127.0.0.1", database="house", user="root", password="123")
        self.db = torndb.Connection(**condic)


class BaseRequestHandler(RequestHandler):

    def set_default_headers(self):
        pass

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            print kwargs.get('Msg', 'None')
            self.render("404.html", errmsg=kwargs['Msg'])
        else:
            self.write("code {0} Msg {1}".format(status_code,  kwargs.get("Msg", "sucess")))
            return

    def on_finish(self):
        super(BaseRequestHandler, self).on_finish()


class IndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        # self.render("new.html")
        # self.send_error(404, Msg=u"页面飞了")
        dbhelper = self.application.db
        result = dbhelper.get("select * from tb_user_info where user_id=%s", self.get_argument("id"))
        usermsg = dict(uname=result["user_name"], umobile=result["user_mobile"], upass=result["user_passwd"])
        self.render("data.html", userdic=[usermsg])

    def post(self, *args, **kwargs):
        name = self.get_argument("name")
        mobile = self.get_argument("mobile")
        upass = self.get_argument("pass")
        db = self.application.db
        id = db.execute("insert into tb_user_info(user_name,user_mobile,user_passwd) values(%s,%s,%s)", name, mobile, upass)
        self.write(str(id))


class Msghandler(RequestHandler):
    def get(self, *args, **kwargs):
        # id = self.get_argument("id")
        db = self.application.db
        ret = db.query("select * from tb_user_info")
        user_dic = []
        for item in ret:
            user_dic.append({
                "uname": item["user_name"],
                "umobile": item["user_mobile"],
                "upass": item["user_passwd"]
            })
        self.render("data.html", userdic=user_dic)


class CookHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.set_cookie(name='bb', value='cc')
        coo = self.get_cookie(name='bb')
        self.write(coo)


if __name__ == "__main__":
    options.parse_config_file("./config.py")
    # staticpath = os.path.join(os.path.dirname(__file__), "statics")  # 静态文件地址默认挂载static
    # templatepath = os.path.join(os.path.dirname(__file__), "templates")
    # conf = dict(debug=True, static_path=staticpath, template_path=templatepath)
    app = BaseApplication([
        (r'/', IndexHandler),
        (r'/m/', Msghandler),
        (r'/c/', CookHandler)
    ], **options.conf)
    curr_ser = HTTPServer(app)
    curr_ser.listen(options.port)
    IOLoop.current().start()