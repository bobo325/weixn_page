#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2018/1/9 13:52
"""
from datetime import datetime

from sqlalchemy import (Column, Integer, String, DateTime)

from flask_app.app import db


# 媒体库
class Media(db.Model):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    name = Column(String(255), default="")  # 文件名称
    type = Column(String(64), default="image")  # 文件类型 image audio video doc zip other
    size = Column(Integer, default=0)  # 文件大小
    url = Column(String(255), default="")  # 文件存储地址
    describe = Column(String(255), default="")  # 文件描述
    uploader = Column(Integer, default=0)  # 文件上传者
    resolution = Column(String(64), default="0*0")  # 文件分辨率 20*20px
    time_length = Column(Integer, default=0)  # 文件时长
    create_time = Column(DateTime)  # 创建时间

    def __init__(self):
        self.create_time = datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'size': self.size,
            'url': self.url,
            'describe': self.describe,
            'uploader': self.uploader,
            'resolution': self.resolution,
            'time_length': self.time_length
        }


# 媒体库配置表
class MediaConf(db.Model):
    __tablename__ = "media_conf"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    type_name = Column(String(64), default="")  # 文件类型名称image audio video doc zip other
    format = Column(String(255), default="")  # 文件格式 多个“，”隔开
    limit_size = Column(Integer, default=0)  # 限制大小 单位字节
    create_time = Column(DateTime)  # 创建时间
    update_time = Column(DateTime)  # 更新时间

    def __init__(self):
        self.create_time = datetime.now()
        self.update_time = datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'type_name': self.type_name,
            'format': self.format,
            'create_time': str(self.create_time),
            'update_time': str(self.update_time),
            'limit_size': self.limit_size
        }
