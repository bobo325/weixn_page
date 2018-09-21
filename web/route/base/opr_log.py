#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/10 17:26
"""
from flask import request

from flask_app import app
from service.base.opration_record import opr_list
from const import msg
from util.common import build_ret


@app.route("/opr/list", methods=["GET"])
def opr_search():
    parameter = request.args.to_dict()
    page = int(parameter.pop('page'))
    limit = int(parameter.pop('limit'))
    cond = {}
    for key, value in parameter.items():
        if value.strip():
            cond[key] = value.rstrip()  # 只除去string右侧的空字符串
    success, resp = opr_list(cond=cond, page=page, limit=limit)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])


