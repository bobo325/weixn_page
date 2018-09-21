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
# import pytest
# from mock import patch
# 
# from const.msg import SYS_SUCCESS
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from model.base.organization import Organization
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
#     org3 = Organization(
#         id=3,
#         name="广东",
#         pid=1,
#         enable=True,
#         description="广东",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org4 = Organization(
#         id=4,
#         name="浙江",
#         pid=1,
#         enable=True,
#         description="浙江",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org5 = Organization(
#         id=5,
#         name="杭州",
#         pid=4,
#         enable=True,
#         description="杭州",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org6 = Organization(
#         id=6,
#         name="金华",
#         pid=4,
#         enable=True,
#         description="金华",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org7 = Organization(
#         id=7,
#         name="广州",
#         pid=3,
#         enable=True,
#         description="广州",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org8 = Organization(
#         id=8,
#         name="深圳",
#         pid=3,
#         enable=True,
#         description="深圳",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org9 = Organization(
#         id=9,
#         name="南昌",
#         pid=2,
#         enable=True,
#         description="南昌",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org10 = Organization(
#         id=10,
#         name="新余",
#         pid=2,
#         enable=True,
#         description="新余",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org11 = Organization(
#         id=11,
#         name="宜春",
#         pid=2,
#         enable=False,
#         description="宜春",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     org12 = Organization(
#         id=12,
#         name="赣州",
#         pid=2,
#         enable=False,
#         description="赣州",
#         creator=1,
#         create_time=datetime.now(),
#         updator=1,
#         update_time=datetime.now()
#     )
#     for i in range(12):
#         org = eval("org%s" % (i + 1))
#         session.add(org)
#     assert len(session.query(Organization).all()) == 12
# 
#     user1 = User(
#         id=1,
#         org_id=1
#     )
# 
#     user2 = User(
#         id=2,
#         org_id=2
#     )
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
# @patch("route.organization.get_cur_user")
# def test_add(mock_user):
#     mock_user.return_value = User(org_id=1)
#     session = session_factory()
#     res_data = util.post(test_client, "/org/add", data={
#         "pid": 1,
#         "name": "dawning7670-广州",
#         "enable": False,
#         "description": "广州部门"
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
# 
#     added_id = 13
#     added_record = session.query(Organization).filter(Organization.id == added_id).one()
#     assert added_record.pid == 1
#     assert added_record.name == "dawning7670-广州"
#     assert added_record.description == "广州部门"
#     assert added_record.enable
# 
# 
# @patch("route.organization.get_cur_user")
# def test_list(mock_user):
#     mock_user.return_value = User(org_id=1)
#     res_data0 = util.get(test_client, "/org/list", headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data1 = util.get(test_client, "/org/list", headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=3)
#     res_data2 = util.get(test_client, "/org/list", headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=4)
#     res_data3 = util.get(test_client, "/org/list", headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=5)
#     res_data4 = util.get(test_client, "/org/list", headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=6)
#     res_data5 = util.get(test_client, "/org/list", headers=HEADERS)
# 
#     data_lens = [12, 5, 3, 3, 1, 1]
#     for i in range(6):
#         res_data = eval("res_data%s" % i)
#         assert res_data['code'] == SYS_SUCCESS.code
#         assert len(res_data['data']) == data_lens[i]
# 
# 
# @patch("route.organization.get_cur_user")
# def test_delete(mock_user):
#     mock_user.return_value = User(org_id=1)
#     session = session_factory()
# 
#     # 组织架构下面有用户
#     res_data = util.post(test_client, "/org/delete", data=[1], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Organization).filter(Organization.id == 1).all()) == 1
# 
#     # 组织架构下面没用户
#     res_data = util.post(test_client, "/org/delete", data=[10], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Organization).filter(Organization.id == 10).all()) == 0
# 
#     # 组织架构ID不存在
#     res_data = util.post(test_client, "/org/delete", data=[222], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Organization).filter(Organization.id == 222).all()) == 0
# 
# 
# @patch("route.organization.get_cur_user")
# def test_update(mock_user):
#     mock_user.return_value = User(org_id=1)
#     session = session_factory()
#     res_data = util.post(test_client, "/org/update", data={
#         "id": 1,
#         "name": "test",
#         "description": "test",
#         "enable": False
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert session.query(Organization).filter(Organization.id == 1).one().enable
# 
#     res_data = util.post(test_client, "/org/update", data={
#         "id": 1,
#         "name": "test",
#         "pid": 3,
#         "description": "test"
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
# 
#     org = session.query(Organization).filter(Organization.id == 1).one()
#     assert org.name == "test"
#     assert org.description == "test"
#     assert org.pid == 3
# 
# 
# @pytest.mark.skip
# @patch("route.organization.get_cur_user")
# def test_enable_and_disable(mock_user):
#     mock_user.return_value = User(org_id=1)
#     session = session_factory()
#     res_data = util.post(test_client, "/org/enable", data=[2], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert all([x.enable for x in session.query(Organization).filter(Organization.id.in_([2, 9, 10, 11, 12])).all()])
# 
#     res_data = util.post(test_client, "/org/disable", data=[3], headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert all([not x.enable for x in session.query(Organization).filter(Organization.id.in_([3, 7, 8])).all()])
