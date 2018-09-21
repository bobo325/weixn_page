# #!/usr/bin/env python
# # encoding: utf-8
# """
# @author: XX
# @time: 2018/1/11 10:32
# """
# from mock import patch
# 
# from const.msg import SYS_SUCCESS
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from model.base.auth import Auth
# from model.base.role import Role
# from model.base.role_auth import RoleAuth
# from model.base.user import User
# from test import engine, util
# 
# # 一定要设置这个key
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
#     role1 = Role(name='root', description='超级管理员', enable=True, creator=0)
#     role2 = Role(name='admin', description='普通管理员', enable=False, creator=0)
#     role3 = Role(name='user', description='用户', enable=True, creator=0)
#     for i in range(3):
#         role = eval("role%s" % (i + 1))
#         session.add(role)
# 
#     auth1 = Auth(name='增加', module='用户管理', opr_url='/user/add')
#     auth2 = Auth(name='修改', module='用户管理', opr_url='/user/update')
#     auth3 = Auth(name='删除', module='用户管理', opr_url='/user/delete')
#     auth4 = Auth(name='查询', module='用户管理', opr_url='/user/list')
#     for i in range(4):
#         auth = eval("auth%s" % (i + 1))
#         session.add(auth)
# 
#     role_auth1 = RoleAuth(role_id=1, auth_id=1)
#     role_auth2 = RoleAuth(role_id=1, auth_id=2)
#     role_auth3 = RoleAuth(role_id=1, auth_id=3)
#     role_auth4 = RoleAuth(role_id=1, auth_id=4)
#     session.add(role_auth1)
#     session.add(role_auth2)
#     session.add(role_auth3)
#     session.add(role_auth4)
# 
#     user1 = User(id=1, org_id=1)
#     user2 = User(id=2, org_id=2)
#     session.add(user1)
#     session.add(user2)
# 
#     session.commit()
# 
#     assert len(session.query(Role).all()) == 3
#     assert len(session.query(RoleAuth).all()) == 4
#     assert len(session.query(User).all()) == 2
# 
# 
# def teardown_function():
#     session = session_factory()
#     session.execute("delete from %s" % Auth.__tablename__)
#     session.execute("delete from %s" % Role.__tablename__)
#     session.execute("delete from %s" % RoleAuth.__tablename__)
#     session.execute("delete from %s" % User.__tablename__)
#     session.commit()
# 
# 
# HEADERS = {
#     "sid": "",
#     "Content-Type": "application/json"
# }
# 
# 
# @patch("route.role.get_cur_user")
# def test_add(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/role/add", data={
#         "name": "admin3",
#         "description": "超级管理员3",
#         "enable": True
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
# 
#     added_record = session.query(Role).filter(Role.name == 'admin3')
#     assert added_record.count() == 1
#     assert len(session.query(Role).all()) == 4
# 
# 
# @patch("route.role.get_cur_user")
# def test_delete(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/role/delete", data={
#         "roles_id": {
#             "0": 4
#         }
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Role).filter(Role.id == 4).all()) == 0
# 
# 
# @patch("route.role.get_cur_user")
# def test_list(mock_user):
#     data0 = {
#         'id': '',
#         'name': '',
#         'enable': '',
#         'page': 1,
#         'limit': 5
#     }
#     data1 = {
#         'id': '',
#         'name': 'r',
#         'enable': 'true',
#         'page': 1,
#         'limit': 10
#     }
#     data2 = {
#         'id': '',
#         'name': '',
#         'enable': '',
#         'page': 2,
#         'limit': 5
#     }
#     data3 = {
#         'id': '',
#         'name': '',
#         'enable': 'false',
#         'page': 1,
#         'limit': 5
#     }
#     mock_user.return_value = User(org_id=1)
#     res_data0 = util.get(client=test_client, url="/role/list", data=data0, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data1 = util.get(client=test_client, url="/role/list", data=data1, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data2 = util.get(client=test_client, url="/role/list", data=data2, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data3 = util.get(client=test_client, url="/role/list", data=data3, headers=HEADERS)
# 
#     data_lens = [3, 2, 0, 1]
#     for i in range(4):
#         res_data = eval("res_data%s" % i)
#         assert res_data['code'] == SYS_SUCCESS.code
#         assert len(res_data['data']) == data_lens[i]
# 
# 
# @patch("route.role.get_cur_user")
# def test_update(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/role/update", data={
#         "id": 1,
#         "name": "super",
#         "description": "超级管理员super"
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     role = session.query(Role).filter(Role.name == 'super').one()
#     assert role.name == "super"
#     assert role.id == 1
# 
# 
# @patch("route.role.get_cur_user")
# def test_enable_and_disable(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/role/disable", data={"roles_id": {"0": 1}}, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Role).filter(Role.enable == 0).all()) == 2
# 
#     res_data = util.post(test_client, "/role/enable", data={"roles_id": {"0": 2}}, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Role).filter(Role.enable == 1).all()) == 2
# 
# 
# @patch("route.role.get_cur_user")
# def test_set_auth(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/role/set_auth", data={
#         "role_id": 2,
#         "auths_id": {"0": 1, "1": 2, "2": 4}
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(RoleAuth).filter(RoleAuth.role_id == 2).all()) == 3
# 
#     res_data = util.post(test_client, "/role/set_auth", data={
#         "role_id": 1,
#         "auths_id": {"0": 1, "1": 3, "2": 4}
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(RoleAuth).filter(RoleAuth.role_id == 1).all()) == 3
# 
#     res_data = util.post(test_client, "/role/set_auth", data={
#         "role_id": 1,
#         "auths_id": {"0": 1, "1": 3}
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(RoleAuth).all()) == 5
