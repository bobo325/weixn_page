#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 16:45
"""
from flask import request

from flask_app import app
from service.base.message import message_entry, user_outbox_list, outbox_message_del, user_outbox_detail, \
    inbox_message_read, inbox_message_detail, inbox_message_del, inbox_message_list, outbox_message_list, \
    outbox_message_detail, user_outbox_message_del
from const import msg
from util.common import build_ret, to_list, get_g


@app.route("/message/outbox/add", methods=["POST"])
def outbox_add():
    current_user = get_g().user
    parameter = request.get_json()
    title = parameter['title']
    context = parameter['context']
    receivers = to_list(parameter['receivers'])
    success, resp = message_entry(receiver=receivers, title=title, context=context, creator=current_user.id)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS)


@app.route("/message/outbox/delete", methods=["POST"])
def outbox_delete():
    current_user = get_g().user
    parameter = request.get_json()
    ids = to_list(parameter['id'])
    success, resp = user_outbox_message_del(ids=ids, oid=current_user.id)
    return build_ret(code=resp)


@app.route("/message/outbox/detail", methods=["POST"])
def outbox_detail():
    parameter = request.get_json()
    mid = int(parameter['id'])
    success, resp = user_outbox_detail(mid=mid)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])


@app.route("/message/outbox/list", methods=["GET"])
def outbox_search():
    parameter = request.args.to_dict()
    page = int(parameter.pop('page'))
    limit = int(parameter.pop('limit'))
    cond = {}
    for key, value in parameter.items():
        if value.strip():
                cond[key] = value
    success, resp = user_outbox_list(cond=cond, page=page, limit=limit)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])


@app.route("/message/inbox/read", methods=["POST"])
def inbox_read():
    parameter = request.get_json()
    mid = to_list(parameter['id'])    # 全部已读传[](转换为{})
    success, resp = inbox_message_read(mid=mid)
    return build_ret(code=resp)


@app.route("/message/inbox/detail", methods=["POST"])
def inbox_detail():
    parameter = request.get_json()
    mid = int(parameter['id'])
    success, resp = inbox_message_detail(mid=mid)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])


@app.route("/message/inbox/delete", methods=["POST"])
def inbox_delete():
    parameter = request.get_json()
    ids = to_list(parameter['id'])
    success, resp = inbox_message_del(mid=ids)
    return build_ret(code=resp)


@app.route("/message/inbox/list", methods=["GET"])
def inbox_list():
    parameter = request.args.to_dict()
    print(parameter)
    page = int(parameter.pop('page'))
    limit = int(parameter.pop('limit'))
    cond = {}
    for key, value in parameter.items():
        if value.strip():
                cond[key] = value
    success, resp = inbox_message_list(cond=cond, page=page, limit=limit)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])


@app.route("/message/manage/delete", methods=["POST"])
def manage_delete():
    current_user = get_g().user
    parameter = request.get_json()
    ids = to_list(parameter['id'])
    success, resp = outbox_message_del(ids=ids, oid=current_user.id)
    return build_ret(code=resp)


@app.route("/message/manage/detail", methods=["POST"])
def manage_detail():
    parameter = request.get_json()
    mid = int(parameter['id'])
    success, resp = outbox_message_detail(mid=mid)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])


@app.route("/message/manage/list", methods=["GET"])
def manage_search():
    parameter = request.args.to_dict()
    page = int(parameter.pop('page'))
    limit = int(parameter.pop('limit'))
    cond = {}
    for key, value in parameter.items():
        if value.strip():
                cond[key] = value
    success, resp = outbox_message_list(cond=cond, page=page, limit=limit)
    if not success:
        return build_ret(code=resp)
    return build_ret(code=msg.SYS_SUCCESS, data=resp['data'], total=resp['total'])