# #!/usr/bin/env python
# # encoding: utf-8
# """
# @author: Tmomy
# @time: 2018/1/12 10:05
# """
# 
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
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
# SYS_SETTING_URL = "/metadata/update"
# SYS_LIST_URL = "/metadata/list"
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
#     session_factory.close_all()
# 
# 
# @session_inject
# def message_search_init(session=None):
#     # 初始化数据
#     pass
# 
# 
# def test_metadata_setting():
#     params = {
#         "area": "basic",
#         "name": "alibaba",
#         "version": "1.0",
#         "company": "阿里巴巴",
#         "logo": "http://alibaba.com",
#         "favicon": "https://www.alibaba.com/favicon.ico"
#     }
#     first_do = util.post(test_client, url=SYS_SETTING_URL, data=params, headers=HEAD)
#     cat_do = util.get(test_client, url=SYS_LIST_URL, headers=HEAD)
#     params2 = params
#     params2['name'] = "al"
#     second_do = util.post(test_client, url=SYS_SETTING_URL, data=params2, headers=HEAD)
#     cat_do2 = util.get(test_client, url=SYS_LIST_URL, headers=HEAD)
#     assert cat_do['data']['name'] == "alibaba", "第1次设置测试结果判定"
#     assert cat_do2['data']['name'] == "al", "第2次设置测试结果判定"
# 
# 
# def test_login_setting():
#     params = {
#         "area": "login",
#         "lock_user_threshold": 5,
#         "captcha_threshold": 3
#     }
#     first_do = util.post(test_client, url=SYS_SETTING_URL, data=params, headers=HEAD)
#     cat_do = util.get(test_client, url=SYS_LIST_URL, headers=HEAD)
#     params2 = params
#     params2['lock_user_threshold'] = 6
#     second_do = util.post(test_client, url=SYS_SETTING_URL, data=params2, headers=HEAD)
#     cat_do2 = util.get(test_client, url=SYS_LIST_URL, headers=HEAD)
#     assert cat_do['data']['lock_user_threshold'] == 5, "第1次设置测试结果判定"
#     assert cat_do2['data']['lock_user_threshold'] == 6, "第2次设置测试结果判定"
