#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 16:26
"""
import datetime

from sqlalchemy import and_

from const import msg
from flask_app.app import db
from model import Message
from model.base.user import User
from model.base.user_pk_message import UserPkMessage
from util.common import get_g
from util.oprlog import opr_data


# 消息发送
def message_entry(title, context, receiver, is_read=1, m_type=1, creator=0):
    on_user = get_g().user
    sender = on_user.id
    if not receiver:
        return False, msg.MESSAGE_UN_RECORD
    messages = []
    new_message = Message(title=title, context=context, m_type=m_type, receiver_num=len(receiver), sender=sender)
    db.session.add(new_message)
    db.session.flush()
    msg_id = new_message.id
    for r in receiver:
        is_exist = User.query.filter(User.id == r).one_or_none()
        if not is_exist:
            return False, msg.MESSAGE_UN_RECORD
        new_user_message = UserPkMessage(msg_id=msg_id, receiver=r, sender=sender)
        new_message.title = title
        messages.append(new_user_message)
    db.session.add(messages)
    db.session.commit()
    od = {}
    nd = {
        'title': title,
        'context': context,
        'sender': sender,
        'receiver': receiver,
        'isread': is_read,
        'm_type': m_type
    }
    opr_data(oid=creator, nd=nd, od=od)
    return True, msg.SYS_SUCCESS


# 系统管理消息查询
def outbox_message_list(sort=None, cond=None, page=1, limit=5):
    offset = (page - 1) * limit
    search_message = Message.query.filter(*outbox_cond_handler(cond)).order_by(
        *message_sort_handler(sort, Message))
    total = search_message.count()
    data = []
    [outbox_msg_handle(ret=data, message=authority) for authority in search_message.offset(offset).limit(limit)]
    resp = {
        'total': total,
        'data': data
    }
    return True, resp


# 系统管理消息详情查看
def outbox_message_detail(mid):
    cond = {
        "id": mid
    }
    return outbox_message_list(cond=cond)


# 系统管理消息删除
def outbox_message_del(ids, oid=0):
    for each in ids:
        is_exist = Message.query.filter(Message.id == int(each)).one_or_none()
        if not is_exist:
            return False, msg.MESSAGE_UN_RECORD
        # 伪删除
        is_exist.is_del = 1
    od = {
        'ids': ids,
    }
    nd = {}
    opr_data(oid=oid, nd=nd, od=od)
    return True, msg.SYS_SUCCESS


# 用户发件箱查询
def user_outbox_list(cond=None, sort=None, page=1, limit=5):
    on_user = get_g().user
    uid = on_user.id
    cond['sender'] = uid
    return outbox_message_list(cond=cond, sort=sort, page=page, limit=limit)


# 用户发件箱消息详情
def user_outbox_detail(mid):
    on_user = get_g().user
    uid = on_user.id
    cond = {
        'id': int(mid),
        'sender': int(uid)
    }
    return outbox_message_list(cond=cond)


# 用户发件箱消息删除
def user_outbox_message_del(ids, oid=0):
    on_user = get_g().user
    uid = on_user.id
    for each in ids:
        is_exist = Message.query.filter(Message.id == int(each), Message.sender == uid).one_or_none()
        if not is_exist:
            return False, msg.MESSAGE_UN_RECORD
        # 伪删除
        is_exist.is_del = 1
    od = {'ids': ids}
    nd = {}
    opr_data(oid=oid, nd=nd, od=od)
    return True, msg.SYS_SUCCESS


# 用户收件箱查询
def inbox_message_list(sort=None, cond=None, page=1, limit=5):
    offset = (page - 1) * limit
    search_message = UserPkMessage.query.filter(*inbox_cond_handler(cond)).order_by(
        *message_sort_handler(sort, UserPkMessage))
    total = search_message.count()
    data = []
    [message_handle(ret=data, message=authority) for authority in search_message.offset(offset).limit(limit)]
    resp = {
        'total': total,
        'data': data
    }
    return True, resp


# 用户收件箱查看详情
def inbox_message_detail(mid):
    on_user = get_g().user
    uid = on_user.id
    is_exist = UserPkMessage.query.filter(UserPkMessage.id == mid, UserPkMessage.receiver == uid).one_or_none()
    if not is_exist:
        return False, msg.MESSAGE_UN_RECORD
    if not is_exist.isread:
        is_exist.isread = 1
        is_exist.read_time = datetime.datetime.now()
        message = Message.query.filter(Message.id == is_exist.msg_id).one_or_none()
        if message:
            message.read_num += 1
    data = []
    user_message_handle(ret=data, message=is_exist)
    if not data:
        return False, msg.MESSAGE_DEL
    total = 1
    resp = {
        'total': total,
        'data': data
    }
    return True, resp


# 用户收件箱标记为已读
def inbox_message_read(mid):
    on_user = get_g().user
    uid = on_user.id
    if not mid:
        # 传来空值 代表全部已读
        un_read_id = UserPkMessage.query.filter(and_(UserPkMessage.isread == 0,
                                                     UserPkMessage.receiver == uid)).all()
        mid = [find_msg.id for find_msg in un_read_id]
    for each in mid:
        un_read_message = UserPkMessage.query.filter(and_(UserPkMessage.id == each, UserPkMessage.isread == 0,
                                                          UserPkMessage.receiver == uid)).one_or_none()
        if not un_read_message:
            return False, msg.MESSAGE_UN_RECORD
        message = Message.query.filter(Message.id == un_read_message.msg_id).one()
        if message.is_del:
            un_read_message.is_del = 1
            return False, msg.MESSAGE_DEL
        elif not un_read_message:
            return False, msg.MESSAGE_UN_RECORD
        # 标记为已读
        un_read_message.isread = 1
        message.read_num += 1
        un_read_message.read_time = datetime.datetime.now()
    return True, msg.SYS_SUCCESS


# 用户收件箱消息删除
def inbox_message_del(mid):
    on_user = get_g().user
    uid = on_user.id
    for each in mid:
        un_read_message = UserPkMessage.query.filter(and_(UserPkMessage.id == each, UserPkMessage.is_del == 0,
                                                          UserPkMessage.receiver == uid)).one_or_none()
        if not un_read_message:
            return False, msg.MESSAGE_UN_RECORD
        # 标记为伪删除
        un_read_message.is_del = 1
    return True, msg.SYS_SUCCESS


def outbox_cond_handler(cond):
    ands = []
    cond['is_del'] = 0
    items = cond.items()
    for key, value in items:
        if key == "id":
            ands.append(and_(Message.id == value))
        elif key == "sender":
            ands.append(and_(Message.sender == value))
        elif key == "title":
            ands.append(and_(Message.title.like("%{}%".format(str(value)))))
        elif key == "is_del":
            ands.append(and_(Message.is_del == value))
        elif key == "sender_time_start":
            ands.append(and_(Message.send_time > value))
        elif key == "sender_time_end":
            ands.append(and_(Message.send_time < value))
    return ands


def inbox_cond_handler(cond):
    on_user = get_g().user
    uid = on_user.id
    ands = []
    cond['receiver'] = uid
    items = cond.items()
    for key, value in items:
        if key == "id":
            ands.append(and_(UserPkMessage.id == value))
        elif key == "receiver":
            ands.append(and_(UserPkMessage.receiver == value))
        if key == "title":
            ands.append(and_(UserPkMessage.title.like("%{}%".format(str(value)))))
        elif key == "isread":
            ands.append(and_(UserPkMessage.isread == value))
        elif key == "is_del":
            ands.append(and_(UserPkMessage.is_del == value))
        elif key == "sender":
            ands.append(and_(UserPkMessage.sender == value))
        elif key == "sender_time_start":
            ands.append(and_(UserPkMessage.send_time > value))
        elif key == "sender_time_end":
            ands.append(and_(UserPkMessage.send_time < value))
    return ands


def message_sort_handler(sort, te):
    if not sort:
        sort = {
            "send_time": "desc"
        }
    sort_mapping = {
        "id": te.id,
        "-id": te.id.desc(),
        "send_time": te.send_time,
        "-send_time": te.send_time.desc()
    }
    sort_list = []
    for key, value in sort.items():
        if value == "desc":
            key = "-" + key
        sort_list.append(sort_mapping[key])
    return tuple(sort_list)


def user_message_handle(ret: list, message: UserPkMessage):
    mes_detail = Message.query.filter(Message.id == message.msg_id).one()
    send_name = User.query.filter(User.id == message.sender).one().username
    receiver_name = User.query.filter(User.id == message.receiver).one().username
    if not mes_detail.is_del:
        message_template = {
            "id": message.id,
            "title": mes_detail.title,
            "context": mes_detail.context,
            "type": mes_detail.m_type,
            "sender_id": message.sender,
            "sender_name": send_name[0],
            "isread": message.isread,
            "receiver": message.receiver,
            "receiver_name": receiver_name[0],
            "send_time": str(message.send_time),
            "read_time": str(message.read_time) if message.isread else ""
        }
        ret.append(message_template)
    else:
        message.is_del = mes_detail.is_del


def message_handle(ret: list, message: UserPkMessage):
    mes_detail = Message.query.filter(Message.id == message.msg_id).one()
    if mes_detail.is_del or message.is_del:
        pass
    else:
        send_name = User.query.filter(User.id == message.sender).one().username
        receiver_name = User.qeury.filter(User.id == message.receiver).one().username
        message_template = {
            "id": message.id,
            "title": mes_detail.title,
            "context": mes_detail.context,
            "type": mes_detail.m_type,
            "sender_id": message.sender,
            "sender_name": send_name[0],
            "receiver": message.receiver,
            "receiver_name": receiver_name[0],
            "is_del": mes_detail.is_del,
            "isread": message.isread,
            "receiver_num": mes_detail.receiver_num,
            "read_num": mes_detail.read_num,
            "send_time": str(message.send_time),
            "read_time": str(message.read_time) if message.isread else ""
        }
        ret.append(message_template)


def outbox_msg_handle(ret: list, message: Message):
    user_msg = UserPkMessage.query.filter(UserPkMessage.msg_id == message.id).all()
    sender_name = None
    sender_id = None
    receivers = []
    for each in user_msg:
        if not sender_id:
            sender_id = each.sender
            sender_name = User.qeury.filter(User.id == sender_id).one().username
        receiver = each.receiver
        receiver_name = User.qeury.filter(User.id == receiver).one().username
        receivers.append({"receiver": receiver, "receiver_name": receiver_name[0], "isread": each.isread})

    message_template = {
        "id": message.id,
        "title": message.title,
        "context": message.context,
        "type": message.m_type,
        "sender_id": sender_id,
        "sender_name": sender_name[0] if sender_name else "",
        "receivers": receivers,
        "is_del": message.is_del,
        "receiver_num": message.receiver_num,
        "read_num": message.read_num,
        "send_time": str(message.send_time)
    }
    ret.append(message_template)
