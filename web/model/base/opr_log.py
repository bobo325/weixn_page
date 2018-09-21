#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 13:14
"""
import datetime
import json

from sqlalchemy import (Column, Integer, String, DateTime, Text)

from flask_app.app import db
from model.base.user import User


class OprLog(db.Model):
    __tablename__ = "opr_log"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    opr_url = Column(String(length=255))  # 操作URL
    browser = Column(String(length=255))  # 浏览器
    platform = Column(String(length=255))  # 系统平台
    uip = Column(String(length=255))  # 用户ip
    old_data = Column(Text)  # 操作前数据
    new_data = Column(Text)  # 操作后数据
    operator = Column(Integer)  # 操作员ID
    success = Column(Integer)  # 操作是否成功
    operate_time = Column(DateTime)  # 创建时间
    module = Column(String(length=255))  # 模块名
    name = Column(String(length=255))  # 权限名

    def __init__(self, opr_url, od, nd, oid, browser, platform, uip, success=0):
        self.opr_url = opr_url
        self.old_data = od
        self.new_data = nd
        self.operator = oid
        self.browser = browser
        self.platform = platform
        self.success = success
        self.uip = uip
        self.operate_time = datetime.datetime.now()

    def to_json(self):
        operator_name = User.query.filter(User.id == self.operator).one_or_none()
        if not operator_name:
            on = "未知"
        else:
            on = operator_name.username
        return {
            'id': self.id,
            'opr_url': self.opr_url,
            'old_data': json.loads(self.old_data),
            'new_data': json.loads(self.new_data),
            'operator': self.operator,
            'browser': self.browser,
            'platform': self.platform,
            'success': self.success,
            'uip': self.uip,
            'model_name': self.module,
            'opr_name': self.name,
            'operator_name': on,
            'operate_time': self.operate_time.strftime("%Y-%m-%d %H:%M:%S") if self.operate_time else ""
        }
