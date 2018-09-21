#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 10:42
"""
# 角色管理
import datetime

from sqlalchemy import and_

from const import msg
from flask_app.app import db
from model.base.auth import Auth
from model.base.role import Role
from model.base.role_auth import RoleAuth
from util.oprlog import opr_data
from service.base import user
from util.date import datetime_format


def role_add(name, description, creator, enable):
    role_check = Role.query.filter(Role.name == name).one_or_none()
    if role_check:
        return msg.SYS_NAME_REPEATED_ERR
    role = Role(name=name, description=description, creator=creator, enable=enable)
    db.session.add(role)
    db.session.commit()
    opr_data(oid=creator, od={}, nd=role.to_json())
    return msg.SYS_SUCCESS


def role_update(id, name, description, updator):
    role_check = Role.query.filter(Role.name == name, Role.id != id).one_or_none()
    if role_check:
        return msg.SYS_NAME_REPEATED_ERR
    role_find = Role.query.filter(Role.id == id).one_or_none()
    if role_find:
        od = role_find.to_json()
        role_find.name = name
        role_find.description = description
        role_find.updator = updator
        role_find.update_time = datetime.datetime.now()
        opr_data(oid=updator, od=od, nd=role_find.to_json())
        return msg.SYS_SUCCESS
    else:
        return msg.SYS_NOT_FOUND


def role_list(id, name, enable, page=None, limit=None):
    search_cond = and_(Role.id == id if id else '',
                       Role.name.like('%' + str(name) + '%'),
                       Role.enable == enable if enable else '')
    result_role = Role.query.filter(search_cond)
    sql_total = result_role.count() if result_role else 0
    if limit is None:
        roles = result_role.order_by(Role.create_time.desc())
    else:
        roles = result_role.order_by(Role.create_time.desc()).offset((page - 1) * limit).limit(limit)
    result = []
    for rl in roles:
        role = {
            'id': rl.id,
            'name': rl.name,
            'description': rl.description,
            'enable': rl.enable,
            'creator': user.get(rl.creator).username,
            'create_time': datetime_format(rl.create_time) if rl.create_time else '',
            'updator': user.get(rl.updator).username,
            'update_time': datetime_format(rl.update_time) if rl.update_time else ''
        }
        auth_list = []
        fk_res = RoleAuth.query \
            .join(Auth, and_(RoleAuth.role_id == rl.id, Auth.id == RoleAuth.auth_id)) \
            .add_entity(Auth) \
            .all()
        for item in fk_res:
            auth_list.append(item[1].to_json())
        role['auth_list'] = auth_list
        result.append(role)
    return result, sql_total


def role_delete(roles_id, oid=0):
    for role_id in roles_id:
        role_find = Role.query.filter(Role.id == role_id).one_or_none()
        if role_find:
            od = role_find.to_json()
            db.session.delete(role_find)
            opr_data(oid=oid, od=od, nd={})
    db.session.commit()
    return msg.SYS_SUCCESS


def role_enable(roles_id, updator):
    od = nd = []
    for role_id in roles_id:
        role_find = Role.query.filter(Role.id == role_id).one_or_none()
        if role_find:
            od.append(role_find.to_json())
            role_find.enable = True
            role_find.updator = updator
            role_find.update_time = datetime.datetime.now()
            nd.append(role_find.to_json())
    opr_data(oid=updator, od={'od': od}, nd={'nd': nd})
    db.session.commit()
    return msg.SYS_SUCCESS


def role_disable(roles_id, updator):
    od = nd = []
    for role_id in roles_id:
        role_find = Role.query.filter(Role.id == role_id).one_or_none()
        if role_find:
            od.append(role_find.to_json())
            role_find.enable = False
            role_find.updator = updator
            role_find.update_time = datetime.datetime.now()
            nd.append(role_find.to_json())
    opr_data(oid=updator, od={'od': od}, nd={'nd': nd})
    db.session.commit()
    return msg.SYS_SUCCESS


def role_set_auth(role_id, auths_id, oid=0):
    od = nd = []
    role_find = Role.query.filter(Role.id == role_id).one_or_none()
    if role_find:
        for auth_id in auths_id:
            auth = Auth.query.filter(Auth.id == auth_id).one_or_none()
            if auth:
                # 三种可能  权限已存在  新增权限  删除（未传）
                role_auth_check = RoleAuth.query.filter(RoleAuth.role_id == role_id,
                                                        RoleAuth.auth_id == auth_id).one_or_none()
                if role_auth_check is None:
                    role_auth = RoleAuth(role_id=role_id, auth_id=auth_id)
                    db.session.add(role_auth)
                    od.append({})
                    nd.append(role_auth.to_json())
        # 删除没勾选的该角色的权限
        role_auth_del = RoleAuth.query.filter(RoleAuth.role_id == role_id,
                                              RoleAuth.auth_id.notin_(auths_id)).all()
        for item in role_auth_del:
            db.session.delete(item)
            od.append(item.to_json())
            nd.append({})
            db.session.delete(item)
        db.session.commit()
        opr_data(oid=oid, od={}, nd={'nd': nd})
        return msg.SYS_SUCCESS
    else:
        db.session.commit()
        return msg.SYS_RECORD_NOT_FOUND


def auth_list_by_role(role_id):
    fk_res = RoleAuth.query \
        .join(Auth, and_(RoleAuth.role_id == role_id, Auth.id == RoleAuth.auth_id, Auth.enable == True)) \
        .add_entity(Auth) \
        .all()
    opr_urls = []
    for item in fk_res:
        opr_urls.append(item[1].opr_url)
    db.session.expunge_all()
    return opr_urls
