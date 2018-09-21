#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 13:10
"""
import json

from flask import request
from sqlalchemy import and_

from const import msg
from flask_app.app import db
from model import OprLog
from model.base.auth import Auth
from model.base.user import User
from util.common import get_g


def opr_entry():
    g = get_g()
    url = getattr(request, 'path') or ""
    od = getattr(g, 'od') if g.get('od') else {}
    nd = getattr(g, 'nd') if g.get('nd') else {}
    oid = getattr(g, 'oid') if g.get('nd') else 0
    if not od and not nd:
        return False, None
    browser = request.user_agent.browser or request.user_agent.string
    platform = request.user_agent.platform or request.user_agent.string
    uip = request.access_route[0] or '127.0.0.1'
    auth = Auth.query.filter(Auth.opr_url == url).one_or_none()
    if auth:
        module = auth.module
        name = auth.name
    else:
        module = ''
        name = ''

    opr_fail = g.opr_fail
    success = 0
    if opr_fail:
        success = 1
    ol_record = OprLog(opr_url=url, od=json.dumps(od), nd=json.dumps(nd), oid=oid, browser=browser, platform=platform,
                       success=success, uip=uip)
    ol_record.name = name
    ol_record.module = module
    db.session.add(ol_record)
    db.session.commit()
    return True, msg.SYS_SUCCESS


def opr_list(sort=None, cond=None, page=1, limit=5):
    offset = (page - 1) * limit
    search_message = OprLog.query.filter(*opr_cond_handler(cond)).order_by(*opr_sort_handler(sort))
    total = search_message.count()
    data = [authority.to_json() for authority in search_message.offset(offset).limit(limit)]
    resp = {
        'total': total,
        'data': data
    }
    return True, resp
    pass


def opr_cond_handler(cond):
    ands = [and_(OprLog.module != "", OprLog.name != "")]
    items = cond.items()
    for key, value in items:
        if key == "id":
            ands.append(and_(OprLog.id == value))
        elif key == "operator":
            ands.append(and_(OprLog.operator == value))
        elif key == "operator_name":
            uid_list = find_like_users_id(username=value)
            if uid_list:
                ands.append(and_(OprLog.operator.in_(uid_list)))
        elif key == "model_name":
            ands.append(and_(OprLog.module.like("%" + value + "%")))
        elif key == "opr_url":
            ands.append(and_(OprLog.opr_url.like("%" + value + "%")))
        elif key == "operate_time_start":
            ands.append(and_(OprLog.operate_time >= value))
        elif key == "operate_time_end":
            ands.append(and_(OprLog.operate_time <= value + " 23:59:59"))
    return ands


def find_like_users_id(username):
    users_id = []
    user_like = User.query.filter(User.username.like('%' + username + '%')).all()
    if user_like:
        users_id = [int(uid.id) for uid in user_like]
    return users_id


def opr_sort_handler(sort):
    if not sort:
        sort = {
            "operate_time": "desc"
        }
    sort_mapping = {
        "operate_time": OprLog.operate_time,
        "-operate_time": OprLog.operate_time.desc()
    }
    sort_list = []
    for key, value in sort.items():
        if value == "desc":
            key = "-" + key
        sort_list.append(sort_mapping[key])
    return tuple(sort_list)
