# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2018-01-09 13:51
"""
from datetime import datetime
from typing import List

from sqlalchemy import and_, text

from config import r_pre, ex_time, web
from const import msg
from flask_app.app import redis as redis_service, db
from model import Metadata
from model.base.organization import Organization
from model.base.role import Role
from model.base.user import User
from service.base import setting as set_service
from service.base.organization import list_by_id, list_all_sub_org
from service.base.role import role_list
from util.common import get_g
from util.oprlog import opr_data
from util.pjwt import en_token


def add(org_id, role_id, username, password, real_name, email,
        tel, enable, description, creator, updator, profile_photo=web['static_avatar'], id=None):
    user = User(id=id, org_id=org_id, role_id=role_id, username=username, password=password,
                real_name=real_name, email=email, tel=tel,
                profile_photo=profile_photo if profile_photo else web['static_avatar'],
                login_error_num=0, enable=enable, description=description,
                creator=creator, create_time=datetime.now(), updator=updator if updator else creator,
                update_time=datetime.now())
    opr_data(oid=creator, od={}, nd=user.to_json())
    db.session.add(user)


def update(id, updator, org_id=None, role_id=None, username=None, real_name=None, email=None, tel=None,
           profile_photo=None, login_error_num=None, description=None, password=None, enable=None,
           last_login_time=None):
    user = get(id)
    if user:
        old_data = user.to_json()
        user.org_id = org_id if org_id is not None else user.org_id
        user.role_id = role_id if role_id is not None else user.role_id
        user.username = username if username is not None else user.username
        user.real_name = real_name if real_name is not None else user.real_name
        user.email = email if email is not None else user.email
        user.tel = tel if tel is not None else user.tel
        user.profile_photo = profile_photo if profile_photo is not None else user.profile_photo
        user.login_error_num = login_error_num if login_error_num is not None else user.login_error_num
        user.description = description if description is not None else user.description
        user.password = password if password is not None else user.password
        user.enable = enable if enable is not None else user.enable
        user.last_login_time = last_login_time if last_login_time is not None else user.last_login_time

        user.updator = updator
        user.update_time = datetime.now()
        opr_data(oid=updator, od=old_data, nd=user.to_json())
        db.session.add(user)


def list(org_id=None, id=None, username=None, password=None, real_name=None, tel=None, enable=None, page=1, limit=10):
    ids = [int(x.id) for x in list_all_sub_org(org_id=org_id)] if org_id else []
    query = User.query.filter(and_(
        User.org_id.in_(ids) if ids != [] else text(""),
        User.id == id if id else text(""),
        User.username == username if username else text(""),
        User.password == password if password else text(""),
        User.real_name.like("%" + str(real_name) + "%") if real_name else text(""),
        User.tel.like("%" + str(tel) + "%") if tel else text(""),
        User.enable == enable if enable is not None else text("")
    ))
    total = query.count()
    user_list = query.order_by(User.create_time.desc()).offset((page - 1) * limit).limit(limit).all()
    data = []
    for it in user_list:
        item = it.to_json()
        if item["creator"]:
            item["creator"] = User.query.filter(User.id == item["creator"]).one().username
        else:
            item["creator"] = ""
        if item["updator"]:
            item["updator"] = User.query.filter(User.id == item["updator"]).one().username
        else:
            item["updator"] = ""
        data.append(item)
    return total, data


def delete(ids: List[int], oid: int):
    for id in ids:
        user = get(id)
        opr_data(oid=oid, od=user.to_json(), nd={})
        db.session.delete(user)


def enable(ids: List[int], updator):
    for id in ids:
        update(id=id, enable=True, login_error_num=0, updator=updator)


def disable(ids: List[int], updator):
    for id in ids:
        update(id=id, enable=False, updator=updator)


def resetpwd(id, old_password, new_password, updator):
    user = get(id)
    if user.password != old_password:
        return False, msg.USER_OLD_PWD_ERR
    update(id=id, password=new_password, updator=updator)
    return True, msg.SYS_SUCCESS


def modify_pwd(id, password, updator):
    update(id=id, password=password, updator=updator)


def get(id: int) -> User:
    user = User.query.filter(User.id == id).one_or_none()
    db.session.expunge_all()
    return user


def get_cur_user() -> User:
    """
    返回当前请求用户
    :return: 返回User对象
    """
    return get(get_g().user.id)


def filter_auth_list(auth_li):
    reset_auth_list = []
    for item in auth_li:
        if item['enable']:
            reset_auth_list.append(item)
    return reset_auth_list


def login(username, password, captcha, captcha_id):
    """
    登录
    :param username: 用户名
    :param password: 密码
    :param captcha: 验证码
    :param captcha_id: 验证码id
    :return: 如正常返回则返回权限数据，否则返回错误码与提示信息
    """
    _, system_data = set_service.system_list()
    if system_data.get('captcha_threshold') is True:
        result, message = check_captcha(captcha, captcha_id)
        if not result:
            return result, message, 0

    user_find = User.query.filter(User.username == username).first()
    metadata = Metadata.query.filter(Metadata.id == 1).one_or_none()
    if user_find:
        if user_find.login_error_num >= metadata.lock_user_threshold:
            return False, msg.USER_LOCKED, user_find.login_error_num
        _, user_list = list(username=username, password=password)
        if not user_list:
            user_find.login_error_num += 1
            db.session.commit()
            return False, msg.USER_PWD_ERR, user_find.login_error_num
        if not user_list[0]['enable']:
            user_find.login_error_num += 1
            db.session.commit()
            return False, msg.USER_DISABLE, user_find.login_error_num
        # query org
        org = list_by_id(user_list[0]['org_id'])
        if not org or not org.enable:
            user_find.login_error_num += 1
            db.session.commit()
            return False, msg.USER_ORG_DISABLE, user_find.login_error_num

        # query user auth list
        role_li, _ = role_list(id=user_list[0]['role_id'], name="", enable=True)
        if not role_li:
            user_find.login_error_num += 1
            return False, msg.USER_ROLE_DISABLE, user_find.login_error_num

        if user_find.login_error_num >= r_pre['login_err_nums']:
            user_find.enable = False
            db.session.commit()
            return False, msg.USER_DISABLE, user_find.login_error_num

        auth_li = role_li[0]['auth_list']
        reset_auth_list = filter_auth_list(auth_li)
        user_find.login_error_num = 0
        # generate token
        token = en_token(
            id=user_list[0]['id'],
            username=user_list[0]['username'],
            org_id=org.id,
            org_name=org.name,
            role_id=role_li[0]['id'],
            role_name=role_li[0]['name']
        )

        data = dict(
            token=str(token, encoding="utf-8"),
            auth_list=reset_auth_list
        )

        # add last login time to db
        update(id=user_list[0]['id'], last_login_time=datetime.now(), login_error_num=0, updator=user_list[0]['id'])
        # add to redis
        redis_service.set(r_pre['token_pre'] + str(user_list[0]['id']), str(token, encoding="utf-8"),
                          ex=ex_time['session_ex'])
        return True, data, user_find.login_error_num
    else:
        return False, msg.USER_PWD_ERR, 0


def check_captcha(captcha, captcha_id):
    rdc_code = redis_service.get(r_pre['user_captcha'] + captcha_id)
    if not rdc_code:
        return False, msg.A_CODE_TIMEOUT
    rdc_code_lower = str(rdc_code.lower(), encoding="utf-8")
    image_code_lower = str(captcha.lower())
    if rdc_code_lower != image_code_lower:
        return False, msg.A_CODE_ERR
    redis_service.delete(r_pre['user_captcha'] + captcha_id)
    return True, msg.SYS_SUCCESS


def logout(id):
    redis_service.delete(r_pre['token_pre'] + id)


def personal(id):
    result = db.session.query(User, Role, Organization).join(Role, and_(Role.id == User.role_id, User.id == id)) \
        .join(Organization, and_(Organization.id == User.org_id)).one()
    user = result.User
    role = result.Role
    org = result.Organization
    data = dict(
        id=user.id,
        username=user.username,
        role_id=role.id,
        role_name=role.name,
        org_id=org.id,
        org_name=org.name,
        real_name=user.real_name,
        email=user.email,
        tel=user.tel,
        description=user.description,
        profile_photo=user.profile_photo
    )
    return data


def personal_update(id, real_name, email, tel, profile_photo, updator):
    update(id=id, real_name=real_name, email=email, tel=tel, profile_photo=profile_photo, updator=updator)


def user_has_permission(id):
    result = User.query \
        .join(Role, and_(Role.id == User.role_id, User.id == id, Role.enable == True, User.enable == True)) \
        .join(Organization, and_(Organization.id == User.org_id, Organization.enable == True)) \
        .all()
    has_permission = True if len(result) > 0 else False
    return has_permission
