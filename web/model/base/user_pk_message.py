#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/2/27 11:26
"""
import datetime

from sqlalchemy import (Column, Integer, String, DateTime)

from flask_app.app import db
from model.base.user import User


class UserPkMessage(db.Model):
    __tablename__ = "user_pk_message"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    msg_id = Column(String(length=255))  # 消息id
    title = Column(String(length=255))  # 消息标题
    m_type = Column(Integer)  # 消息类型
    receiver = Column(Integer)  # 接收人id
    sender = Column(Integer)  # 发送人id
    isread = Column(Integer)  # 是否已读  1/0 == 已读/未读
    is_del = Column(Integer, default=0)  # 伪删除 1/0 == 删除/为删除
    send_time = Column(DateTime)  # 发送时间
    read_time = Column(DateTime)  # 读取

    def __init__(self, msg_id, receiver, sender, isread=0, m_type=1):
        self.msg_id = msg_id
        self.receiver = receiver
        self.sender = sender
        self.isread = isread
        self.m_type = m_type
        self.send_time = datetime.datetime.now()
        self.read_time = datetime.datetime.now()

    def to_json(self, session=None):
        send = session.query(User).filter(User.id == self.sender).one_or_none()
        re = session.query(User).filter(User.id == self.receiver).one_or_none()
        if not send:
            sender_name = ""
        else:
            sender_name = send.username
        if not re:
            receiver_name = ""
        else:
            receiver_name = send.username
        return {
            'id': self.id,
            'receiver': self.receiver,
            'sender': self.sender,
            'isread': self.isread,
            'm_type': self.m_type,
            'sender_name': sender_name,
            'receiver_name': receiver_name,
            'send_time': str(self.send_time),
            'read_time': str(self.read_time)
        }
