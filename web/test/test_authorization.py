# # encoding: utf-8
# 
# """
# @version: 1.0
# @author: dawning
# @contact: dawning7670@gmail.com
# @time: 2018/1/9 17:12
# """
# from datetime import datetime
# 
# from flask import g
# 
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from intercept.before_request import authorization
# from model.base.auth import Auth
# from model.base.organization import Organization
# from model.base.role import Role
# from model.base.role_auth import RoleAuth
# from model.base.user import User
# from test import engine, mock_rdc
# # 一定要设置这个key
# from util.oprlog import opr_data
# 
# app.config[TESTING_CONFIG_KEY] = True
# test_client = app.test_client()
# 
# 
# def setup_module():
#     # 创表
#     ModelBase.metadata.create_all(engine)
# 
# 
# def teardown_module():
#     session_factory.close_all()
# 
# 
# def setup_function():
#     session = session_factory()
#     # 初始化数据
#     """
#     1-全国
#         2-江西
#             9-南昌
#             10-新余
#             11-宜春
#             12-赣州
#         3-广东
#             7-广州
#             8-深圳
#         4-浙江
#             5-杭州
#             6-金华
#     """
#     org1 = Organization(
#         id=1,
#         name="全国",
#         pid=0,
#         enable=True,
#         description="全国",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org2 = Organization(
#         id=2,
#         name="江西",
#         pid=1,
#         enable=True,
#         description="江西",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
# 
#     role1 = Role(
#         name="管理员",
#         description="admin role",
#         enable=True,
#         creator=1
#     )
# 
#     user1 = User(
#         org_id=1,
#         role_id=1,
#         username="admin",
#         password="123456",
#         real_name="管理员大大",
#         email="1@qq.com",
#         tel="1888999234",
#         profile_photo="/opt/1.jpg",
#         description="admin12345",
#         enable=True
#     )
# 
#     user2 = User(
#         org_id=1,
#         role_id=1,
#         username="admin2",
#         password="123456",
#         real_name="管理员大大2",
#         email="2@qq.com",
#         tel="1888999235",
#         profile_photo="/opt/2.jpg",
#         description="admin12346",
#         enable=True
#     )
# 
#     auth1 = Auth(1)
#     auth1.id = 1
#     auth1.enable = 1
#     auth1.name = "添加"
#     auth1.opr_url = "/user/add"
#     auth1.module = "用户"
# 
#     auth2 = Auth(1)
#     auth2.id = 2
#     auth2.enable = 1
#     auth2.name = "查询"
#     auth2.opr_url = "/user/list"
#     auth2.module = "用户"
# 
#     auth3 = Auth(1)
#     auth3.id = 3
#     auth3.enable = 1
#     auth3.name = "查询"
#     auth3.opr_url = "/org/list"
#     auth3.module = "组织架构"
# 
#     auth4 = Auth(1)
#     auth4.id = 4
#     auth4.enable = 1
#     auth4.name = "添加"
#     auth4.opr_url = "/org/add"
#     auth4.module = "组织架构"
# 
#     auth5 = Auth(1)
#     auth5.id = 5
#     auth5.enable = 1
#     auth5.name = "查询"
#     auth5.opr_url = "/role/list"
#     auth5.module = "角色"
# 
#     auth6 = Auth(1)
#     auth6.id = 6
#     auth6.enable = 1
#     auth6.name = "查询"
#     auth6.opr_url = "/auth/add"
#     auth6.module = "权限项"
# 
#     role_auth1 = RoleAuth(role_id=1, auth_id=1)
#     role_auth2 = RoleAuth(role_id=1, auth_id=2)
#     role_auth3 = RoleAuth(role_id=1, auth_id=3)
#     role_auth4 = RoleAuth(role_id=1, auth_id=4)
#     role_auth5 = RoleAuth(role_id=1, auth_id=5)
#     role_auth6 = RoleAuth(role_id=1, auth_id=6)
# 
#     for i in range(2):
#         org = eval("org%s" % (i + 1))
#         session.add(org)
#     assert len(session.query(Organization).all()) == 2
# 
#     session.add(role1)
#     assert len(session.query(Role).all()) == 1
# 
#     session.add(user1)
#     session.add(user2)
# 
#     assert len(session.query(User).all()) == 2
# 
#     for i in range(6):
#         auth = eval("auth%s" % (i + 1))
#         session.add(auth)
#     assert len(session.query(Auth).all()) == 6
# 
#     for i in range(6):
#         role_auth = eval("role_auth%s" % (i + 1))
#         session.add(role_auth)
#     assert len(session.query(RoleAuth).all()) == 6
#     session.commit()
# 
# 
# def teardown_function():
#     session = session_factory()
#     session.execute("delete from %s" % Auth.__tablename__)
#     session.execute("delete from %s" % RoleAuth.__tablename__)
#     session.execute("delete from %s" % Role.__tablename__)
#     session.execute("delete from %s" % User.__tablename__)
#     session.execute("delete from %s" % Organization.__tablename__)
#     session.commit()
# 
# 
# HEADERS = {
#     "authorization": "a.b.c",
#     "Content-Type": "application/json",
#     "sid": 1
# }
# 
# redis_dic = {
#     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWQiOiIxIiwib3JnX2lkIjoiMSIsIm9yZ19uYW1lIjoiXHU1MTY4XHU1NmZkIiwicm9sZV9pZCI6IjEiLCJyb2xlX25hbWUiOiJyMSIsImlhdCI6MTUxNTY3Mjk4My42NTUyMTEyLCJleHAiOjE1MTY1MzY5ODMuNjU1MjExMn0.ycz5zNmaVkiasqF43Me_WbU9IViE04OVQSqOk8wfPsw": b"bFfL4yjy",
#     "u_t_1": b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWQiOiIxIiwib3JnX2lkIjoiMSIsIm9yZ19uYW1lIjoiXHU1MTY4XHU1NmZkIiwicm9sZV9pZCI6IjEiLCJyb2xlX25hbWUiOiJyMSIsImlhdCI6MTUxNTY3Mjk4My42NTUyMTEyLCJleHAiOjE1MTY1MzY5ODMuNjU1MjExMn0.ycz5zNmaVkiasqF43Me_WbU9IViE04OVQSqOk8wfPsw"
# }
# 
# 
# def get_side_effect(key):
#     return redis_dic[key]
# 
# 
# def set_side_effect(key, value, ex):
#     redis_dic[key] = value
# 
# 
# def test_auth():
#     mock_rdc.get = get_side_effect
#     mock_rdc.set = set_side_effect
#     mock_rdc.get.return_value = b'bFfL4yjy'
#     with app.test_request_context(path="/user/list", method="POST", headers={
#         'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWQiOiIxIiwib3JnX2lkIjoiMSIsIm9yZ19uYW1lIjoiXHU1MTY4XHU1NmZkIiwicm9sZV9pZCI6IjEiLCJyb2xlX25hbWUiOiJyMSIsImlhdCI6MTUxNTY3Mjk4My42NTUyMTEyLCJleHAiOjE1MTY1MzY5ODMuNjU1MjExMn0.ycz5zNmaVkiasqF43Me_WbU9IViE04OVQSqOk8wfPsw'}):
#         opr_data(0, {}, {})
#         g.opr_fail = True
#         assert authorization()
