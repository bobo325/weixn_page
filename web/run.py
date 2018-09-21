# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2018-01-08 16:01
"""
from flask_cors import CORS

from config import web
from flask_app import app

if __name__ == '__main__':
    """
    app.debug=True时，定时任务或其他脚本会被执行了2次，原因是flask会多开一个线程来监测项目的变化
    解决方案可以将app.dubug修改为False或添加参数use_reloader=False
    """
    if web['debug']:
        CORS(app, supports_credentials=True)
        app.run(host=web['ip'], port=web['port'], debug=True, threaded=True)
    else:
        app.run(host=web['ip'], port=web['port'])
