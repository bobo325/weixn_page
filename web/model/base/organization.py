# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/9 11:48
"""

from sqlalchemy import Column, DateTime, Integer, String, Boolean

from flask_app.app import db


class Organization(db.Model):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=255))
    pid = Column(Integer)
    enable = Column(Boolean)
    description = Column(String(length=255))
    creator = Column(Integer)
    create_time = Column(DateTime)
    updator = Column(Integer)
    update_time = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "pid": self.pid,
            "enable": self.enable,
            "description": self.description,
            "creator": self.creator,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updator": self.updator,
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
