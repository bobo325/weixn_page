#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 17:17
"""
import json

from flask import request, make_response

from config import r_pre, ex_time
from const import msg
from const import test
from flask_app.app import redis as redis_service
from flask_app import app
from model.base.user import User
from service.base.role import auth_list_by_role
from service.base.user import user_has_permission
from util.common import get_g, build_ret
from util.log_builder import logging
from util.pjwt import de_token

no_login_list = [
    '/system_base/captcha',
    '/metadata/list',
    '/user/login'
]


@app.before_request
def prepare_request():
    """
    所有拦截器执行的代码都放到这一个方法里
    :return:
    """
    request.params = get_request_args()
    logging.info('request ip is: [%s], url is: [%s], args is: [%s]', request.remote_addr, request.path, request.params)

    # 不管是不是单元测试都需要使用的拦截器
    init_opr_entry_env()

    if not is_running_in_unit_test():
        """
        这里设置的拦截器会在运行单元测试时跳过
        单元测试执行时需要设置
        app.config[TESTING_CONFIG_KEY] = True
        
        这个函数返回的非None值会被作为请求的Response返回给客户端
        
        拦截器建议写成一个函数的形式，例如：
        def check_auth():
            return None
        
        然后添加到这里的时候就这样写
        ret = check_auth()
        if ret is not None:
            return ret
        """
        ret = authorization()
        if ret is not None:
            return ret


def get_request_args():
    args = {}
    if request.method == "GET":
        args = request.args.to_dict()
        # parse json
        for k, v in args.items():
            if args[k].startswith("{"):
                args[k] = json.loads(v)
    elif request.method == "POST":
        if not request.data and len(request.data):
            args = json.loads(request.data)
    return args


def init_opr_entry_env():
    g = get_g()
    g.od = {}
    g.nd = {}
    g.oid = 0
    g.opr_fail = False


def is_running_in_unit_test():
    return test.TESTING_CONFIG_KEY in app.config and app.config[test.TESTING_CONFIG_KEY]


def authorization():
    path = request.path
    if not path_check(path) and str(request.method) not in ['OPTIONS']:
        token = request.headers.get('token')
        re_bool, info = token_check(token=token)
        if not re_bool:
            return info
        init_user(info)
        re_bool, resp = login_status_check(id=info['id'], token=token)
        if not re_bool:
            return resp
        role_id = info['role_id']
        check_result = authority_check(id=info['id'], role_id=role_id)
        if not check_result:
            return make_response(build_ret(msg.A_NO_AUTHOR))


def init_user(token_info):
    """
    初始化用户基本信息，包括（id, username, role_id, org_id）
    :param token_info:
    :return:
    """
    g = get_g()
    g.user = User(id=token_info['id'], username=token_info['username'], role_id=token_info['role_id'],
                  org_id=token_info['org_id'])


def path_check(path):
    if path in no_login_list:
        return True
    else:
        return False


def token_check(token):
    account_info = de_token(token)
    if not account_info:
        return False, make_response(build_ret(msg.A_TIMEOUT))
    return True, account_info


def login_status_check(id, token):
    redis_token = redis_service.get(r_pre['token_pre'] + id)
    if not redis_token:
        return False, make_response(build_ret(msg.A_TIMEOUT))
    if redis_token.decode() != token:
        return False, make_response(build_ret(msg.A_SIGNED))
    redis_service.set(r_pre['token_pre'] + id, redis_token, ex=ex_time['session_ex'])
    return True, True


def authority_check(id, role_id):
    # 检查用户角色、组织是否正常
    has_permission = user_has_permission(id)
    if not has_permission:
        return False

    # 检查明细权限
    path = str(request.path)
    author_list = auth_list_by_role(role_id)

    if not author_list:
        return False
    if path not in author_list:
        return False
    return True
