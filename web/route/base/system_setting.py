#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 14:24
"""
from flask import request

from flask_app import app
from service.base.setting import system_setting, login_setting, system_list
from const import msg
from util.common import build_ret, get_g


@app.route("/metadata/update", methods=["POST"])
def metadata_setting():
    parameter = request.get_json()
    current_user = get_g().user
    area = parameter['area']
    if area == "basic":
        name = parameter['name']
        version = parameter['version']
        company = parameter['company']
        logo = parameter['logo']
        favicon = parameter['favicon']
        success, resp = system_setting(name=name, version=version, company=company, logo=logo, favicon=favicon, oid=current_user.id)
    elif area == "login":
        lut = parameter['lock_user_threshold']
        ct = parameter['captcha_threshold']
        success, resp = login_setting(lut=lut, ct=ct, oid=current_user.id)
    else:
        resp = msg.SYS_FAIL
    return build_ret(code=resp)


@app.route("/metadata/list", methods=["GET"])
def metadata_list():
    success, resp = system_list()
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp)
