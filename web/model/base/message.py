#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 16:09
"""
import datetime

from sqlalchemy import (Column, Integer, String, DateTime, Text)

from flask_app.app import db
from model.base.user import User


class Message(db.Model):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    title = Column(String(length=255))  # 消息标题
    m_type = Column(Integer)  # 消息类型
    context = Column(Text)  # 消息主体
    receiver_num = Column(Integer)  # 接收人数
    sender = Column(Integer)  # 发送人
    is_del = Column(Integer)  # 伪删除 1/0 == 删除/为删除
    read_num = Column(Integer)  # 已读人数
    send_time = Column(DateTime)  # 发送时间
    read_time = Column(DateTime)  # 最后一次更新时间

    def __init__(self, title, sender, context, receiver_num=0, is_del=0, read_num=0, m_type=1):
        self.title = title
        self.context = context
        self.sender = sender
        self.receiver_num = receiver_num
        self.is_del = is_del
        self.read_num = read_num
        self.m_type = m_type
        self.send_time = datetime.datetime.now()
        self.read_time = datetime.datetime.now()

    # todo
    def to_json(self, session=None):
        send = session.query(User).filter(User.id == 0).one_or_none()
        re = session.query(User).filter(User.id == 0).one_or_none()
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
            'title': self.title,
            'context': self.context,
            'receiver_num': self.receiver_num,
            'is_del': self.is_del,
            'read_num': self.read_num,
            'm_type': self.m_type,
            'sender_name': sender_name,
            'receiver_name': receiver_name,
            'send_time': str(self.send_time),
            'read_time': str(self.read_time)
        }
