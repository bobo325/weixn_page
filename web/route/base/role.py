#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 11:39
"""
from flask import request

from flask_app import app
from service.base.role import *
from util.common import build_ret, to_list, get_g


@app.route('/role/add', methods=['POST'])
def role_add_func():
    """{
      "name": "admin",
      "description": "超级管理员",
      "enable": true
    }"""
    params = request.get_json()
    creator = get_g().user
    name = params['name']
    description = params['description']
    enable = params['enable'] if params['enable'] is not None else ''
    res_code = role_add(name=name, description=description, creator=creator.id, enable=enable)
    return build_ret(code=res_code)


@app.route('/role/update', methods=['POST'])
def role_update_func():
    """
        {
          "id": 1,
          "name": "admin",
          "description": "超级管理员"
        }
    """
    updator = get_g().user
    params = request.get_json()
    name = params['name']
    description = params['description']
    id = int(params['id']) if params['id'] is not None else ''
    res_code = role_update(id=id, name=name, description=description, updator=updator.id)
    return build_ret(res_code)


@app.route('/role/list', methods=['GET'])
def role_list_func():
    """
    {
      "id": 0,
      "name": '',
      "enable": true,
      "page": 2,
      "limit": 2
    }
    """
    params = request.args.to_dict()
    id = int(params.get('id').lstrip()) if params.get('id') else ''
    name = params.get('name').lstrip() if params.get('name') else ''
    if params.get('enable'):
        if params.get('enable') == 'true':
            enable = True
        elif params.get('enable') == 'false':
            enable = False
        else:
            enable = ''
    else:
        enable = ''
    page = int(params.get('page')) if params.get('page') else None
    limit = int(params.get('limit')) if params.get('limit') else None
    data, total = role_list(id=id, name=name, enable=enable, page=page, limit=limit)
    return build_ret(code=msg.SYS_SUCCESS, data=data, total=total)


@app.route('/role/delete', methods=['POST'])
def role_delete_func():
    """{"roles_id": {"0": 2, "1": 3} }  所有需要删除的角色id列表"""
    updator = get_g().user
    params = request.get_json()
    roles_id = to_list(params['roles_id'])
    res_code = role_delete(roles_id=roles_id, oid=updator.id)
    return build_ret(res_code)


@app.route('/role/set_auth', methods=['POST'])
def role_set_auth_func():
    """{
        "role_id": 1,
        "auths_id": {"0": 2, "1": 3}  #  所有需要设置的权限id列表
    }  """
    updator = get_g().user
    params = request.get_json()
    role_id = int(params['role_id'])
    auths_id = to_list(params['auths_id'])
    res_code = role_set_auth(role_id=role_id, auths_id=auths_id, oid=updator.id)
    return build_ret(res_code)


@app.route('/role/enable', methods=['POST'])
def role_enable_func():
    """{"roles_id": {"0": 2, "1": 3} }  所有需要启用的角色id列表"""
    updator = get_g().user
    params = request.get_json()
    roles_id = to_list(params['roles_id'])
    res_code = role_enable(roles_id=roles_id, updator=updator.id)
    return build_ret(res_code)


@app.route('/role/disable', methods=['POST'])
def role_disable_func():
    """{"roles_id": {"0": 2, "1": 3} }  所有需要禁用的角色id列表"""
    updator = get_g().user
    params = request.get_json()
    roles_id = to_list(params['roles_id'])
    res_code = role_disable(roles_id=roles_id, updator=updator.id)
    return build_ret(res_code)
