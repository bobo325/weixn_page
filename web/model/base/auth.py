#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 10:14
"""
import datetime
from sqlalchemy import (Column, Integer, String, Boolean, DateTime)

from flask_app.app import db


class Auth(db.Model):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True, autoincrement=True)      # 主键ID
    name = Column(String(length=255))                               # 权限名称
    module = Column(String(length=255))                             # 模块名称
    opr_url = Column(String(length=255))                            # 权限操作
    need_auditing = Column(Boolean)                                 # 是否需要审核
    enable = Column(Boolean)                                        # 启用禁用
    creator = Column(Integer)                                       # 创建人id
    create_time = Column(DateTime)                                  # 创建时间
    updator = Column(Integer)                                       # 更新人id
    update_time = Column(DateTime)                                  # 更新时间

    def __init__(self, name='', module='', opr_url='', need_auditing=False, enable=False, creator=0):
        self.name = name
        self.module = module
        self.opr_url = opr_url
        self.need_auditing = need_auditing
        self.enable = enable
        self.creator = creator
        self.updator = creator
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'module': self.module,
            'opr_url': self.opr_url,
            'enable': self.enable,
            'need_auditing': self.need_auditing,
            'creator': self.creator,
            'create_time': str(self.create_time) if self.create_time else '',
            'updator': self.updator,
            'update_time': str(self.update_time) if self.update_time else ''
        }