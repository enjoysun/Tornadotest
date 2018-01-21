# coding:utf-8
import os
port = 8000
subject = ['math', 'english']
staticpath = os.path.join(os.path.dirname(__file__), "statics")  # 静态文件地址默认挂载static
templatepath = os.path.join(os.path.dirname(__file__), "templates")
conf = dict(debug=True, static_path=staticpath, template_path=templatepath)