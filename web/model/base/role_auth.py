#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/1/9 10:19
"""
from sqlalchemy import (Column, Integer)

from flask_app.app import db


class RoleAuth(db.Model):
    __tablename__ = "role_auth"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键ID
    role_id = Column(Integer)  # 角色id
    auth_id = Column(Integer)  # 权限id

    def __init__(self, role_id, auth_id):
        self.role_id = role_id
        self.auth_id = auth_id

    def to_json(self):
        return {
            'id': self.id,
            'role_id': self.role_id,
            'auth_id': self.auth_id
        }
