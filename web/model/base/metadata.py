#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 10:55
"""
import datetime

from sqlalchemy import (Column, Integer, String, DateTime, Boolean)

from flask_app.app import db


class Metadata(db.Model):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    name = Column(String(length=255))  # 名称
    version = Column(String(length=255))  # 系统版本
    company = Column(String(length=255))  # 公司名称
    logo = Column(String(length=255))  # 系统logo
    favicon = Column(String(length=255))  # 系统图标
    lock_user_threshold = Column(Integer)  # 登陆失败多少次锁定用户
    captcha_threshold = Column(Boolean)  # 是否需要验证码 True 需要 False 不需要
    create_time = Column(DateTime)  # 创建时间
    modify_time = Column(DateTime)  # 最后一次更新时间

    def __init__(self, name="", version="", company="", logo="", favicon="", lut=0, ct=False):
        self.name = name
        self.version = version
        self.company = company
        self.logo = logo
        self.favicon = favicon
        self.lock_user_threshold = lut
        self.captcha_threshold = ct
        self.create_time = datetime.datetime.now()
        self.modify_time = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'logo': self.logo,
            'version': self.version,
            'favicon': self.favicon,
            'lock_user_threshold': self.lock_user_threshold,
            'captcha_threshold': self.captcha_threshold,
            'create_time': str(self.create_time),
            'modify_time': str(self.modify_time)
        }
