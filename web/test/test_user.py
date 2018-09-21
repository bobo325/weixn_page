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
# from mock import patch
#
# from const.msg import SYS_SUCCESS
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from model.base.organization import Organization
# from model.base.role import Role
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
#     role1.create_time = datetime.now()
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
#     session.commit()
#
#
# def teardown_function():
#     session = session_factory()
#     session.execute("delete from %s" % Organization.__tablename__)
#     session.execute("delete from %s" % Role.__tablename__)
#     session.execute("delete from %s" % User.__tablename__)
#     session.commit()
#
#
# HEADERS = {
#     "authorization": "a.b.c",
#     "Content-Type": "application/json",
#     "sid": 1
# }
#
#
# @patch("route.user.get_cur_user")
# def test_add(mock_user):
#     mock_user.return_value = User(id=1)
#     session = session_factory()
#     res_data = util.post(test_client, "/user/add", data={
#         "org_id": 1,
#         "role_id": 1,
#         "username": "kelvin",
#         "password": "123456",
#         "real_name": "人民",
#         "email": "2@qq.com",
#         "tel": "1888999235",
#         "profile_photo": "/opt/2.jpg",
#         "description": "kelvinaa1234",
#         "enable": True
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#
#     username = "kelvin"
#     added_record = session.query(User).filter(User.username == username).one()
#     print(added_record.to_json())
#     assert added_record.org_id == 1
#     assert added_record.real_name == "人民"
#
#
# @patch("route.user.get_cur_user")
# def test_list(mock_user):
#     mock_user.return_value = User(id=1)
#     res_data0 = util.get(test_client, "/user/list", data={
#         "username": "admin",
#         "limit": 10,
#         "org_id": 1,
#         "enable": ""
#     }, headers=HEADERS)
#
#     assert res_data0['code'] == SYS_SUCCESS.code
#     assert len(res_data0['data']) == 2
#
#
# @patch("route.user.get_cur_user")
# def test_delete(mock_user):
#     mock_user.return_value = User(id=1)
#     session = session_factory()
#     res_data = util.post(test_client, "/user/delete", data=[1], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Organization).filter(Organization.id == 1).all()) == 1
#
#
# @patch("route.user.get_cur_user")
# def test_update(mock_user):
#     mock_user.return_value = User(id=1)
#     session = session_factory()
#     # 用户修改
#     res_data = util.post(test_client, "/user/update", data={
#         "id": 1,
#         "org_id": 3,
#         "role_id": 3,
#         "username": "test",
#         "real_name": "test123",
#         "tel": "111111111111",
#         "email": "123@qq.com",
#         "description": "test",
#         "profile_photo": "/opt/33.jpg",
#         "enable": False
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#
#     user = session.query(User).filter(User.id == 1).one()
#     assert user.username == "test"
#     assert user.description == "test"
#
#     # 个人中心修改
#     res_data = util.post(test_client, "/user/personal_update", data={
#         "id": 1,
#         "real_name": "test567",
#         "tel": "222222",
#         "email": "123@qq.com",
#         "profile_photo": "/opt/33.jpg"
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#
#     res_data1 = util.get(test_client, "/user/get", data={
#         "id": 1
#     }, headers=HEADERS)
#
#     assert res_data1['data'][0]['real_name'] == "test567"
#     assert res_data1['data'][0]['tel'] == "222222"
#
#     # 个人中心修改密码
#     res_data = util.post(test_client, "/user/resetpwd", data={
#         "old_password": "123456",
#         "new_password": "222222"
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#
#     res_data2 = util.get(test_client, "/user/get", data={
#         "id": 1
#     }, headers=HEADERS)
#
#     assert res_data2['data'][0]['tel'] == "222222"
#
#
# @patch("route.user.get_cur_user")
# def test_enable_and_disable(mock_user):
#     mock_user.return_value = User(id=1)
#     session = session_factory()
#     res_data = util.post(test_client, "/user/enable", data=[1], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#
#     res_data = util.post(test_client, "/user/disable", data=[1], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
