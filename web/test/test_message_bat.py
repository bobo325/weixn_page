# #!/usr/bin/env python
# # encoding: utf-8
# """
# @author: Tmomy
# @time: 2018/1/10 15:01
# """
# import datetime
# 
# from mock import patch
# 
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from model import Message
# from model.base.user import User
# from test import engine, util
# from util.decorator import session_inject
# 
# app.config[TESTING_CONFIG_KEY] = True
# test_client = None
# HEAD = {
#     "sid": "",
#     "Content-Type": "application/json"
# }
# 
# MESSAGE_LIST_URL = "/message/list"
# MESSAGE_ADD_URL = "/message/add"
# MESSAGE_DEL_URL = "/message/delete"
# 
# 
# def setup_module():
#     app.config['TESTING'] = True
#     app.config['CSRF_ENABLED'] = False
#     global test_client
#     test_client = app.test_client()
# 
#     # 创表
#     ModelBase.metadata.create_all(engine)
#     message_search_init()
# 
# 
# def teardown_module():
#     session = session_factory()
#     session.execute("delete from %s" % User.__tablename__)
#     session.commit()
#     session_factory.close_all()
# 
# 
# @session_inject
# def message_search_init(session=None):
#     # 初始化数据
#     test_data = [
#         {
#             "title": "test1",
#             "context": "context1",
#             "receiver": 1,
#             "sender": 2,
#             "create_time": "2018-01-09 17:34:04"
#         },
#         {
#             "title": "test2",
#             "context": "context2",
#             "receiver": 1,
#             "sender": 3,
#             "create_time": "2018-01-08 17:34:04"
#         },
#         {
#             "title": "test2",
#             "context": "context1",
#             "receiver": 2,
#             "sender": 2,
#             "create_time": "2018-01-04 17:34:04"
#         }
#     ]
#     user1 = User(
#         id=3,
#         org_id=1
#     )
# 
#     user2 = User(
#         id=2,
#         org_id=2
#     )
#     user3 = User(
#         id=1,
#         org_id=3
#     )
#     session.add(user1)
#     session.add(user2)
#     session.add(user3)
#     for msg in test_data:
#         m = Message(title=msg['title'], context=msg['context'], receiver=msg['receiver'], sender=msg['sender'])
#         m.send_time = datetime.datetime.strptime(msg['create_time'], "%Y-%m-%d %H:%M:%S")
#         session.add(m)
#     session.commit()
# 
# 
# # search all
# def test_message_search_all():
#     params = {
#         "page": 1,
#         "limit": 5,
#         "title": "",
#         "receiver": "",
#         "sender": "",
#         "sender_time_start": "",
#         "sender_time_end": ""
#     }
#     all_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params, headers=HEAD)
#     assert all_data['total'] == 3, "查询所有记录测试结果"
# 
# 
# def test_message_search_date_limit():
#     params = {
#         "page": 1,
#         "limit": 5,
#         "title": "",
#         "receiver": "",
#         "sender": "",
#         "sender_time_start": "",
#         "sender_time_end": ""
#     }
#     params1 = params
#     params1['sender_time_start'] = "2018-01-03"
#     params1['sender_time_end'] = "2018-01-04"
#     no_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params1, headers=HEAD)
# 
#     params2 = params
#     params2['sender_time_start'] = "2018-01-03"
#     params2['sender_time_end'] = "2018-01-05"
#     one_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params2, headers=HEAD)
#     assert one_data['total'] == 1, "一条记录在日期范围查询测试结果"
#     assert no_data['total'] == 0, "无记录在日期范围查询测试结果"
# 
# 
# @patch("route.message.get_cur_user")
# def test_message_add(mock_user):
#     mock_user.return_value = User(id=1)
#     params = {
#         "page": 1,
#         "limit": 5,
#         "title": "",
#         "receiver": "",
#         "sender": "",
#         "sender_time_start": "",
#         "sender_time_end": ""
#     }
#     test_data = {
#         "title": "paty",
#         "context": "hahaha",
#         "receivers": [2, 3]
#     }
#     before_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params, headers=HEAD)
#     one_data = util.post(test_client, url=MESSAGE_ADD_URL, data=test_data, headers=HEAD)
#     after_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params, headers=HEAD)
#     before_total = before_data['total']
#     after_total = after_data['total']
#     assert one_data['code'] == 0, "消息添加请求是否请求成功"
#     assert after_total == before_total + 2, "消息是否准确入库"
# 
# 
# def test_message_delete():
#     params = {
#         "page": 1,
#         "limit": 5,
#         "title": "",
#         "receiver": "",
#         "sender": "",
#         "sender_time_start": "",
#         "sender_time_end": ""
#     }
#     pass
#     params['title'] = u"test1"
#     test_data = {
#         'id': [1]
#     }
#     before_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params, headers=HEAD)
#     do_data = util.post(test_client, url=MESSAGE_DEL_URL, data=test_data, headers=HEAD)
#     after_data = util.get(test_client, url=MESSAGE_LIST_URL, data=params, headers=HEAD)
#     assert before_data['total'] == 1, "操作前数据是否存在"
#     assert do_data['code'] == 0, "消息删除请求是否请求成功"
#     assert after_data['total'] == 0, "消息是否准确删除"
