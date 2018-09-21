# encoding: utf-8
'''
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2018-01-09 13:58
'''
from flask import request

from const import msg
from flask_app import app, build_ret
from service.base import user
from util.common import to_list, tran_bool, get_g


@app.route('/user/login', methods=['POST'])
def user_login():
    args = request.json
    result, data, count = user.login(
        username=args['username'],
        password=args['password'],
        captcha=args.get('captcha'),
        captcha_id=request.headers.get('captcha-id') if request.headers else None
    )

    if result:
        return build_ret(msg.SYS_SUCCESS, data=data, total=count)
    else:
        return build_ret(data, total=count)


@app.route('/user/logout', methods=['POST'])
def user_logout():
    current_user = get_g().user
    user.logout(current_user.id)
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/add', methods=['POST'])
def user_add():
    current_user = get_g().user
    args = request.json
    _, u_list = user.list(username=args['username'])
    if len(u_list) > 0:
        return build_ret(msg.USER_EXISTS)

    user.add(
        org_id=args['org_id'],
        role_id=args['role_id'],
        username=args.get('username'),
        password=args['password'],
        real_name=args.get('real_name'),
        email=args['email'],
        tel=args['tel'],
        enable=args['enable'],
        description=args['description'],
        creator=current_user.id,
        updator=None,
        profile_photo=args.get('profile_photo')
    )
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/update', methods=['POST'])
def user_update():
    current_user = get_g().user
    args = request.json
    user.update(
        id=args.get('id', 0),
        org_id=args.get('org_id', 0),
        role_id=args.get('role_id', 0),
        username=args['username'],
        real_name=args['real_name'],
        email=args['email'],
        tel=args['tel'],
        description=args['description'],
        updator=current_user.id,
        profile_photo=args.get('profile_photo')
    )
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/list', methods=['GET'])
def user_list():
    args = request.args
    total, data = user.list(
        org_id=args.get('org_id'),
        id=args.get('id'),
        username=args.get('username'),
        real_name=args.get('real_name'),
        tel=args.get('tel'),
        enable=tran_bool(args.get('enable')),
        page=int(args.get('page', 1)),
        limit=int(args.get('limit', 10))
    )
    return build_ret(msg.SYS_SUCCESS, total=total, data=data)


@app.route('/user/delete', methods=['POST'])
def user_delete():
    current_user = get_g().user
    user.delete(
        ids=to_list(request.json), oid=current_user.id
    )
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/enable', methods=['POST'])
def user_enable():
    current_user = get_g().user
    user.enable(ids=to_list(request.json), updator=current_user.id)
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/disable', methods=['POST'])
def user_disable():
    current_user = get_g().user
    user.disable(ids=to_list(request.json), updator=current_user.id)
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/resetpwd', methods=['POST'])
def user_resetpwd():
    current_user = get_g().user
    args = request.json
    _, code = user.resetpwd(
        id=current_user.id,
        old_password=args['old_password'],
        new_password=args['new_password'],
        updator=current_user.id
    )
    return build_ret(code)


@app.route('/user/modifypwd', methods=['POST'])
def user_modify_pwd():
    current_user = get_g().user
    args = request.json
    user.modify_pwd(
        id=args['id'],
        password=args['password'],
        updator=current_user.id
    )
    return build_ret(msg.SYS_SUCCESS)


@app.route('/user/get', methods=['GET'])
def user_get():
    data = user.get(id=get_g().user.id)
    data = [data.to_json()]
    return build_ret(msg.SYS_SUCCESS, data=data)


@app.route('/user/personal', methods=['GET'])
def user_personal():
    data = user.personal(
        get_g().user.id
    )
    data = [data]
    return build_ret(msg.SYS_SUCCESS, data=data)


@app.route('/user/personal_update', methods=['POST'])
def user_personal_update():
    current_user = get_g().user
    args = request.json
    user.personal_update(
        id=current_user.id,
        real_name=args['real_name'],
        email=args['email'],
        tel=args['tel'],
        profile_photo=args.get('profile_photo'),
        updator=current_user.id
    )
    return build_ret(msg.SYS_SUCCESS)
