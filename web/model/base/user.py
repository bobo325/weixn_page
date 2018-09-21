# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2018-01-09 10:48
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from flask_app.app import db


class User(db.Model):
    __tablename__ = 'user'
    # 主键ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色ID
    org_id = Column(Integer)
    # 角色id
    role_id = Column(Integer)
    # 用户名
    username = Column(String(length=255))
    # 密码
    password = Column(String(length=255))
    # 真实姓名
    real_name = Column(String(length=255))
    # 邮箱
    email = Column(String(length=255))
    # 电话
    tel = Column(String(length=255))
    # 个人头像
    profile_photo = Column(String(length=255))
    # 登录错误次数
    login_error_num = Column(Integer)
    # 启用禁用true,false
    enable = Column(Boolean)
    # 描述
    description = Column(String(length=255))
    # 上次登录时间
    last_login_time = Column(DateTime)
    # 创建人
    creator = Column(Integer)
    # 创建时间
    create_time = Column(DateTime)
    # 更新人
    updator = Column(Integer)
    # 最后一次更新时间
    update_time = Column(DateTime)

    def to_json(self):
        return {
            'id': self.id,
            'org_id': self.org_id,
            'role_id': self.role_id,
            'username': self.username,
            'real_name': self.real_name,
            'email': self.email,
            'tel': self.tel,
            'profile_photo': self.profile_photo,
            'login_error_num': self.login_error_num,
            'enable': self.enable,
            'description': self.description,
            'last_login_time': str(self.last_login_time) if self.last_login_time else "",
            'creator': self.creator,
            'create_time': str(self.create_time) if self.create_time else "",
            'updator': self.updator,
            'update_time': str(self.update_time) if self.update_time else ""
        }

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()
