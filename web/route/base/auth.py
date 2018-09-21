#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 11:39
"""
from flask import request

from flask_app import app
from service.base.auth import *
from util.common import build_ret, to_list, get_g


@app.route('/auth/list', methods=['GET'])
def auth_list_func():
    """
    {
      "id": 1,
      "module": "用户",
      "opr_url": "/user/add"
      "enable": true,
      "page": 2,
      "limit": 2
    }
    """
    params = request.args.to_dict()
    id = int(params.get('id').lstrip()) if params.get('id') else ''
    module = params.get('module').lstrip() if params.get('module') else ''
    opr_url = params.get('opr_url').lstrip() if params.get('opr_url') else ''
    enable = params.get('enable') if params.get('enable') else ''
    print(enable)
    page = int(params.get('page')) if params.get('page').lstrip() else None
    limit = int(params.get('limit')) if params.get('limit').lstrip() else None
    data, total = auth_list(id=id, module=module, opr_url=opr_url, enable=enable, page=page, limit=limit)
    return build_ret(code=msg.SYS_SUCCESS, data=data, total=total)


@app.route('/auth/enable', methods=['POST'])
def auth_enable_func():
    """{"auths_id": {"0": 2, "1": 3} }  需要启用的权限id列表"""
    updator = get_g().user
    params = request.get_json()
    auths_id = to_list(params['auths_id'])
    res_code = auth_enable(auths_id=auths_id, updator=updator.id)
    return build_ret(res_code)


@app.route('/auth/disable', methods=['POST'])
def auth_disable_func():
    """{"auths_id": {"0": 2, "1": 3} }  需要禁用的权限id列表"""
    updator = get_g().user
    params = request.get_json()
    auths_id = to_list(params['auths_id'])
    res_code = auth_disable(auths_id=auths_id, updator=updator.id)
    return build_ret(res_code)


@app.route('/auth/audit', methods=['POST'])
def auth_audit_func():
    """{
        "need_auditing": true,     # true  开启审核  false  关闭审核
        "auths_id": {              # 审核的权限id列表
            "0": 2,
            "1": 3
        }
    }"""
    updator = get_g().user
    params = request.get_json()
    need_auditing = params['need_auditing']
    auths_id = to_list(params['auths_id'])
    res_code = auth_audit(need_auditing=need_auditing, auths_id=auths_id, updator=updator.id)
    return build_ret(res_code)
