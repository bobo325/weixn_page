#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 10:43
"""
# 权限管理
import datetime

from const import msg
from model.base.auth import Auth
from util.oprlog import opr_data
from service.base import user
from util.date import datetime_format


def auth_list(id, module, opr_url, enable, page, limit):
    # 暂时过滤掉站内信/收件箱、发件箱
    result_auth = Auth.query.filter(Auth.id == id if id else '',
                                    Auth.module.like('%' + str(module) + '%'),
                                    Auth.opr_url.notlike('%' + '/message' + '%'),
                                    Auth.opr_url.like('%' + str(opr_url) + '%'),
                                    Auth.enable == enable if enable else '')
    sql_total = result_auth.count() if result_auth else 0
    if limit is None:
        auths = result_auth.order_by(Auth.create_time.desc()).all()
    else:
        auths = result_auth.order_by(Auth.create_time.desc()).limit(limit).offset((page - 1) * limit).all()
    result = [{
            'id': auth.id,
            'name': auth.name,
            'module': auth.module,
            'opr_url': auth.opr_url,
            'enable': auth.enable,
            'need_auditing': auth.need_auditing,
            'creator': user.get(auth.creator).username,
            'create_time': datetime_format(auth.create_time) if auth.create_time else '',
            'updator': user.get(auth.updator).username,
            'update_time': datetime_format(auth.update_time) if auth.update_time else ''
        } for auth in auths]
    return result, sql_total


def auth_enable(auths_id, updator):
    od = nd = []
    for auth_id in auths_id:
        auth_find = Auth.query.filter(Auth.id == auth_id).one_or_none()
        if auth_find:
            od.append(auth_find.to_json())
            auth_find.enable = True
            auth_find.updator = updator
            auth_find.update_time = datetime.datetime.now()
            nd.append(auth_find.to_json())
    opr_data(oid=updator, od={'od': od}, nd={'nd': nd})
    return msg.SYS_SUCCESS


def auth_disable(auths_id, updator):
    od = nd = []
    for auth_id in auths_id:
        auth_find = Auth.query.filter(Auth.id == auth_id).one_or_none()
        if auth_find:
            od.append(auth_find.to_json())
            auth_find.enable = False
            auth_find.updator = updator
            auth_find.update_time = datetime.datetime.now()
            nd.append(auth_find.to_json())
    opr_data(oid=updator, od={'od': od}, nd={'nd': nd})
    return msg.SYS_SUCCESS


def auth_audit(need_auditing, auths_id, updator):
    od = nd = []
    for auth_id in auths_id:
        auth_find = Auth.query.filter(Auth.id == auth_id).one_or_none()
        if auth_find:
            od.append(auth_find.to_json())
            auth_find.need_auditing = need_auditing
            auth_find.updator = updator
            auth_find.update_time = datetime.datetime.now()
            nd.append(auth_find.to_json())
    opr_data(oid=updator, od={'od': od}, nd={'nd': nd})
    return msg.SYS_SUCCESS
