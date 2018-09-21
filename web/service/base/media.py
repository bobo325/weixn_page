#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2018/1/9 14:02
"""
import datetime

from sqlalchemy import or_, and_

from flask_app.app import db
from model.base.media import Media, MediaConf
from model.base.user import User
from util.common import datetime_offset_by_month
from util.oprlog import opr_data


def list_media_type():
    """
    查询媒体类型
    :return:
    """
    sql_result = MediaConf.query.all()
    result = [i.to_json() for i in sql_result]
    return result


def modify_media_type(data: dict, updator: int):
    """
    修改媒体类型
    :param data:{
        "type_name":"image",
        "limit_size":789,
        "format":"jpg,png"
    }
    :return:
    """
    sql_result = MediaConf.query.filter(MediaConf.type_name == data["type_name"]).one()
    old = sql_result.to_json()
    sql_result.update_time = datetime.datetime.now()
    sql_result.limit_size = data["limit_size"]
    sql_result.format = data["format"]
    opr_data(oid=updator, nd=sql_result.to_json(), od=old)


def add_media(data: dict, creator: int):
    """
    添加媒体
    :param data:{
        "name":"name",
        "type":"type",
        "size":"size",
        "url":"url",
        "uploader":"uploader",
        "resolution":"resolution",
        "time_length":"time_length"
    }
    :return:
    """
    model = Media()
    for key, value in data.items():
        setattr(model, key, value)
        db.session.add(model)
    opr_data(oid=creator, nd=model.to_json(), od={})


def modify_media(data: dict, updator: int):
    """
    编辑媒体
    :param data:{
        "id":789
        "name":"name",
        "describe":"describe"
    }
    :return:
    """
    sql_result = Media.queyr.filter(Media.id == data["id"]).one()
    old = sql_result.to_json()
    sql_result.name = data["name"]
    sql_result.describe = data["describe"]
    opr_data(oid=updator, nd=sql_result.to_json(), od=old)


def list_media(data: dict):
    """
    媒体库查询
    :param data:{
        "key_word": "jj",
        "type": "jj",
        "month": "2017-12"
    }
    :return:
    """
    # 时间格式转换
    if data["month"] != "":
        month_format = datetime.datetime.strptime(data["month"], '%Y-%m')
        start_time = datetime.datetime.strftime(month_format, '%Y-%m-%d %H:%M:%S')
        end_time = datetime_offset_by_month(month_format, 1)
    else:
        start_time = None
        end_time = None

    # 分页
    limit = int(data['limit'])
    offset = (int(data['page']) - 1) * limit

    sql_result = Media.query \
        .join(User, and_(Media.uploader == User.id, Media.type.like('%' + str(data["type"]) + '%'),
                         Media.create_time.between(start_time, end_time) if start_time is not None else "",
                         or_(Media.name.like('%' + str(data["key_word"]) + '%'),
                             Media.describe.like('%' + str(data["key_word"]) + '%'))
                         )).with_entities(User.username, Media)

    sql_total = sql_result.count()
    sql_content = sql_result.order_by(Media.create_time.desc()).limit(limit).offset(offset)
    items = []
    for i in sql_content:
        item = i[1].to_json()
        item["uploader_name"] = User.query.get(i[1].uploader).real_name
        items.append(item)
    return sql_total, items


def delete_media(ids: list, oid: int):
    """
    删除媒体库
    :param ids: type(int)
    :return:
    """
    for media_id in ids:
        sql_result = Media.query.filter(Media.id == media_id).one_or_none()
        if sql_result:
            db.session.delete(sql_result)
            opr_data(oid=oid, nd={}, od=sql_result.to_json())


def detail_media(id):
    """
    媒体库详情
    :param id: type(int)
    :return:
    """
    sql_result = Media.query.filter(Media.id == int(id)).one_or_none()
    if sql_result:
        user_result = User.query.filter(User.id == sql_result.uploader).one()
        item = sql_result.to_json()
        item["uploader_name"] = user_result.username
        return item
    return False
