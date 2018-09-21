# #!/usr/bin/env python
# # encoding: utf-8
# """
# @author: leason
# @time: 2018/1/10 14:45
# """
# from mock import patch
# 
# from config import web
# from const.msg import SYS_SUCCESS
# from const.test import TESTING_CONFIG_KEY
# from db.db_api import ModelBase
# from db.postgres import session_factory
# from flask_app import app
# from model.base.media import MediaConf, Media
# from model.base.user import User
# from test import engine, util
# # 一定要设置这个key
# from util import file
# 
# app.config[TESTING_CONFIG_KEY] = True
# test_client = None
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
#     # 路径修改
#     web["pic_read"] = ".."
#     web["upload_path"] = "../static_file/upload"
# 
# 
# def teardown_module():
#     session_factory.close_all()
# 
# 
# def setup_function():
#     session = session_factory()
#     conf_items = [
#         {
#             "type_name": "image",
#             "limit_size": 5242880,
#             "format": "jpg,png"
#         },
#         {
#             "type_name": "audio",
#             "limit_size": 52428800,
#             "format": "mp3"
#         }, {
#             "type_name": "video",
#             "limit_size": 524288000,
#             "format": "mp4"
#         }, {
#             "type_name": "doc",
#             "limit_size": 52428800,
#             "format": "doc,docx"
#         }, {
#             "type_name": "other",
#             "limit_size": 5242880,
#             "format": "7z"
#         }, {
#             "type_name": "zip",
#             "limit_size": 5242880,
#             "format": "zip"
#         }
#     ]
# 
#     for conf_item in conf_items:
#         media_conf = MediaConf()
#         for key, value in conf_item.items():
#             setattr(media_conf, key, value)
#         session.add(media_conf)
#     session.commit()
#     assert len(session.query(MediaConf).all()) == 6
# 
#     media_items = [
#         {
#             "name": "test-1",
#             "uploader": 1,
#             "type": "image",
#             "size": 789,
#             "url": "url",
#             "resolution": "50X100"
#         }, {
#             "name": "test-2",
#             "uploader": 1,
#             "type": "doc",
#             "size": 789,
#             "url": "url"
#         }, {
#             "name": "test-3",
#             "uploader": 1,
#             "type": "image",
#             "size": 789,
#             "url": "url",
#             "resolution": "50X100"
#         }, {
#             "name": "test-4",
#             "uploader": 1,
#             "type": "doc",
#             "size": 789,
#             "url": "url"
#         }
#     ]
#     for media_item in media_items:
#         media = Media()
#         for key, value in media_item.items():
#             setattr(media, key, value)
#         session.add(media)
#     user = User(id=1, username="leason")
#     session.add(user)
#     session.commit()
#     assert len(session.query(Media).all()) == 4
# 
# 
# def teardown_function():
#     session = session_factory()
#     session.execute("delete from %s" % MediaConf.__tablename__)
#     session.execute("delete from %s" % Media.__tablename__)
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
# def test_conf_list():
#     res_data = util.get(test_client, "/mediaType/list", headers=HEADERS)
#     assert len(res_data["data"]) == 6
# 
# 
# def test_conf_modify():
#     session = session_factory()
#     res_data = util.post(test_client, "/mediaType/update", data={
#         "type_name": "image",
#         "limit_size": 651131,
#         "format": "jpg,png,gif"
#     }, headers=HEADERS)
# 
#     assert res_data["code"] == SYS_SUCCESS.code
#     assert session.query(MediaConf).filter(MediaConf.type_name == "image").one().limit_size == 651131
#     assert session.query(MediaConf).filter(MediaConf.type_name == "image").one().format == "jpg,png,gif"
# 
# 
# @patch("route.media.get_cur_user")
# def test_media_upload(mock_user):
#     mock_user.return_value = User(id=1)
#     session = session_factory()
#     HEADERS["Content-Type"] = "multipart/form-data"
#     # test type img
#     with open(file.get_file_path('test', 'static', 'media', 'test_image.png'), 'rb') as f:
#         data = {
#             "file": [
#                 (f, "test_image.png", "test_image")
#             ]
#         }
#         res_data = util.post(test_client, "/media/upload", data=data, headers=HEADERS)
# 
#     assert res_data["code"] == SYS_SUCCESS.code
#     assert session.query(Media).filter(Media.name == "test_image").count() == 1
#     assert session.query(Media).filter(Media.name == "test_image").one().resolution == "954X387"
#     assert session.query(Media).filter(Media.name == "test_image").one().uploader == 1
#     # test type doc
#     with open(file.get_file_path('test', 'static', 'media', 'test_doc.docx'), 'rb') as f:
#         data = {
#             "file": [
#                 (f, "test_doc.docx", "test_doc")
#             ]
#         }
#         res_data = util.post(test_client, "/media/upload", data=data, headers=HEADERS)
# 
#     assert res_data["code"] == SYS_SUCCESS.code
#     assert session.query(Media).filter(Media.name == "test_doc").count() == 1
#     assert session.query(Media).filter(Media.name == "test_doc").one().type == "doc"
# 
# 
# def test_media_list():
#     res_data_0 = util.get(test_client, "/media/list", data={
#         "limit": 2,
#         "page": 1,
#         "key_word": "",
#         "type": "",
#         "month": ""
#     }, headers=HEADERS)
# 
#     res_data_1 = util.get(test_client, "/media/list", data={
#         "limit": 10,
#         "page": 1,
#         "key_word": "1",
#         "type": "",
#         "month": ""
#     }, headers=HEADERS)
# 
#     res_data_2 = util.get(test_client, "/media/list", data={
#         "limit": 10,
#         "page": 1,
#         "key_word": "test",
#         "type": "image",
#         "month": ""
#     }, headers=HEADERS)
# 
#     res_data_3 = util.get(test_client, "/media/list", data={
#         "limit": 10,
#         "page": 1,
#         "key_word": "test",
#         "type": "image",
#         "month": "2018-01"
#     }, headers=HEADERS)
# 
#     result = [2, 1, 2, 2]
# 
#     assert res_data_0["total"] == 4
#     for i in range(4):
#         res_data = eval("res_data_%s" % i)
#         assert res_data['code'] == SYS_SUCCESS.code
#         assert len(res_data['data']) == result[i]
# 
# 
# def test_media_modify():
#     session = session_factory()
#     HEADERS["Content-Type"] = "application/json"
#     res_data = util.post(test_client, "/media/update", data={
#         "id": 1,
#         "name": "leason",
#         "describe": "test"
#     }, headers=HEADERS)
# 
#     assert res_data["code"] == SYS_SUCCESS.code
#     assert session.query(Media).filter(Media.id == 1).one().name == "leason"
#     assert session.query(Media).filter(Media.id == 1).one().describe == "test"
# 
# 
# def test_media_delete():
#     session = session_factory()
#     res_data = util.post(test_client, "/media/delete", data={
#         "ids": [1, 3]
#     }, headers=HEADERS)
# 
#     assert res_data["code"] == SYS_SUCCESS.code
#     assert session.query(Media).filter(Media.id == 1).count() == 0
#     assert session.query(Media).filter(Media.id == 3).count() == 0
#     assert session.query(Media).count() == 2
# 
# 
# def test_media_detail():
#     session = session_factory()
#     res_data = util.get(test_client, "/media/detail", data={
#         "id": 2
#     }, headers=HEADERS)
#     assert res_data["code"] == SYS_SUCCESS.code
#     assert res_data["data"]["name"] == session.query(Media).filter(Media.id == 2).one().name
