#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 9:55
"""
import datetime

from sqlalchemy import (Column, Integer, String, DateTime, Boolean)

from flask_app.app import db


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    name = Column(String(length=255))  # 角色名称
    description = Column(String(length=255))  # 描述
    enable = Column(Boolean)  # 启用禁用
    creator = Column(Integer)  # 创建人id
    create_time = Column(DateTime)  # 创建时间
    updator = Column(Integer)  # 更新人id
    update_time = Column(DateTime)  # 更新时间

    def __init__(self, name, description, creator, enable=False):
        self.name = name
        self.description = description
        self.enable = enable
        self.creator = creator
        self.updator = creator
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'enable': self.enable,
            'creator': self.creator,
            'create_time': str(self.create_time) if self.create_time else '',
            'updator': self.updator,
            'update_time': str(self.update_time) if self.update_time else ''
        }
