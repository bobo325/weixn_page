# from mock import patch
# 
# from const.msg import SYS_SUCCESS
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from model.base.auth import Auth
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
#     auth1 = Auth(name='增加', module='用户管理', opr_url='/user/add', need_auditing=True, enable=True)
#     auth2 = Auth(name='修改', module='用户管理', opr_url='/user/update', need_auditing=False, enable=False)
#     auth3 = Auth(name='删除', module='用户管理', opr_url='/user/delete', need_auditing=True, enable=False)
#     auth4 = Auth(name='增加', module='角色管理', opr_url='/role/add', need_auditing=True, enable=True)
#     for i in range(4):
#         auth = eval("auth%s" % (i + 1))
#         session.add(auth)
# 
#     user1 = User(id=1, org_id=1)
#     user2 = User(id=2, org_id=2)
#     session.add(user1)
#     session.add(user2)
# 
#     session.commit()
# 
#     assert len(session.query(Auth).all()) == 4
#     assert len(session.query(User).all()) == 2
# 
# 
# def teardown_function():
#     session = session_factory()
#     session.execute("delete from %s" % Auth.__tablename__)
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
# @patch("route.auth.get_cur_user")
# def test_list(mock_user):
#     data0 = {
#         "id": '',
#         "module": "",
#         "opr_url": "",
#         "enable": '',
#         "need_auditing": '',
#         "page": 1,
#         "limit": 5
#     }
#     data1 = {
#         "id": '',
#         "module": "用户",
#         "opr_url": "",
#         "enable": '',
#         "need_auditing": 'true',
#         "page": 1,
#         "limit": 5
#     }
#     data2 = {
#         "id": '',
#         "module": "角色",
#         "opr_url": "add",
#         "enable": '',
#         "need_auditing": '',
#         "page": 1,
#         "limit": 5
#     }
#     data3 = {
#         "id": '',
#         "module": "",
#         "opr_url": "",
#         "enable": 'false',
#         "need_auditing": 'true',
#         "page": 1,
#         "limit": 5
#     }
#     data4 = {
#         "id": '',
#         "module": "",
#         "opr_url": "",
#         "enable": '',
#         "need_auditing": 'true',
#         "page": 2,
#         "limit": 5
#     }
#     mock_user.return_value = User(org_id=1)
#     res_data0 = util.get(client=test_client, url="/auth/list", data=data0, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data1 = util.get(client=test_client, url="/auth/list", data=data1, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data2 = util.get(client=test_client, url="/auth/list", data=data2, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data3 = util.get(client=test_client, url="/auth/list", data=data3, headers=HEADERS)
# 
#     mock_user.return_value = User(org_id=2)
#     res_data4 = util.get(client=test_client, url="/auth/list", data=data4, headers=HEADERS)
# 
#     data_lens = [4, 3, 1, 2, 0]
#     for i in range(5):
#         res_data = eval("res_data%s" % i)
#         assert res_data['code'] == SYS_SUCCESS.code
#         assert len(res_data['data']) == data_lens[i]
# 
# 
# @patch("route.auth.get_cur_user")
# def test_enable_and_disable(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/auth/disable", data={"auths_id": {"0": 1}}, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Auth).filter(Auth.enable == 0).all()) == 3
# 
#     res_data = util.post(test_client, "/auth/enable", data={"auths_id": {"0": 2, "1": 3}}, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Auth).filter(Auth.enable == 1).all()) == 3
# 
# 
# @patch("route.auth.get_cur_user")
# def test_auth_audit(mock_user):
#     mock_user.return_value = User()
#     session = session_factory()
#     res_data = util.post(test_client, "/auth/audit", data={
#         "need_auditing": 0,
#         "auths_id": {  # 审核的权限id列表
#             "0": 3,
#             "1": 4
#         }
#     }, headers=HEADERS)
#     assert res_data['code'] == SYS_SUCCESS.code
#     assert len(session.query(Auth).filter(Auth.need_auditing == 0).all()) == 3
