# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/9 15:04
"""
import sys

import const
from config import web
from const import Code
from flask_app import app
from util.common import build_ret
from util.log_builder import logging


@app.errorhandler(Exception)
def internal_error(_):
    if web['debug']:
        exc_type, exc_info, _ = sys.exc_info()
        msg = "%s %s" % (exc_type, exc_info)
        response = build_ret(Code(code=const.CODE_SYS_ERROR.code, msg=msg))
    else:
        response = build_ret(const.CODE_SYS_ERROR)
    logging.error("exception occurs in request", exc_info=1)
    return response


# 处理404页面
@app.errorhandler(404)
def not_found(_):
    response = build_ret(const.SYS_NOT_FOUND)
    return response


# 处理400页面
@app.errorhandler(400)
def bad_request(_):
    response = build_ret(const.SYS_INVALID_REQUEST)
    logging.error("invalid request", exc_info=1)
    return response
