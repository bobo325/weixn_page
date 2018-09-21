#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2018/1/9 9:59
"""
import datetime
import hashlib
import json
import uuid

from flask import current_app

from const import Code


def build_ret(code: Code, total=0, data: list = None, sec_msg: str = None):
    """
    生成请求响应json
    :param sec_msg:
    :param code: type(dict) 信息
    :param total: type(int) 数据总数(用于分页)
    :param data: type(list) 数据
    :return: format of json is:
    {
        "data": []
        "total": 0,
        "msg": "",
        "code": 0
    }
    """
    if data is None:
        data = []
    msg = "%s%s" % (code.msg, sec_msg) if sec_msg else code.msg
    dic = {
        "data": data,
        "total": total,
        "msg": msg,
        "code": code.code
    }
    # 处理data里的None 转换为空字符串
    tran_none_data(data)
    return current_app.response_class(
        (json.dumps(dic, ensure_ascii=False)),
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )


def build_ret_one(code: Code, data: dict = None, sec_msg: str = None):
    """
    生成请求响应json
    :param sec_msg:
    :param code: 错误类
    :param data: 数据
    :return: format of json is:
    {
        "data": {}
        "msg": "",
        "code": 0
    }
    """
    if data is None:
        data = {}
    msg = "%s%s" % (code.msg, sec_msg) if sec_msg else code.msg
    dic = {
        "data": data,
        "msg": msg,
        "code": code.code
    }
    # 处理data里的None 转换为空字符串
    tran_none_data(data)
    return current_app.response_class(
        (json.dumps(dic, ensure_ascii=False)),
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )


def tran_none_data(dic_json):
    """
    原来的data中可能存在json格式数据，所以在转换为json格式数据后再转回dict做空元素处理
    :param dic_json:
    :return:
    """
    if isinstance(dic_json, dict):
        for key in dic_json:
            fill_data(dic_json, key)
    elif isinstance(dic_json, list):
        for data in dic_json:
            for key in data:
                fill_data(data, key)


def fill_data(dic_json: dict, key):
    if isinstance(dic_json[key], list):
        for li in dic_json[key]:
            tran_none_data(li)
    elif dic_json[key] is None or dic_json[key] == 'None':
        dic_json[key] = ""


def date_time(day_offset=0, seconds_offset=0, microseconds_offset=0, milliseconds_offset=0, minutes_offset=0,
              hours_offset=0, weeks_offset=0, fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间
    :param day_offset:
    :param seconds_offset:
    :param microseconds_offset:
    :param milliseconds_offset:
    :param minutes_offset:
    :param hours_offset:
    :param weeks_offset:
    :param fmt: 格式化字符串
    :return:
    """
    _date_time = datetime.datetime.now() + datetime.timedelta(days=day_offset,
                                                              seconds=seconds_offset,
                                                              microseconds=microseconds_offset,
                                                              milliseconds=milliseconds_offset,
                                                              minutes=minutes_offset,
                                                              hours=hours_offset,
                                                              weeks=weeks_offset)
    return _date_time.strftime(fmt)


def md5(str):
    """
    生成MD5值
    :param str:
    :return:
    """
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def get_uuid():
    """
    由MAC地址、当前时间戳、随机数生成(83be7c1e152d11e78f8cd8cb8aca49be)
    :return: type(String)
    """
    return str(uuid.uuid1()).replace('-', '')


def get_g():
    g_proxy = object()
    try:
        from flask import g
        g_proxy = g
        g_proxy.info = True
    except:
        pass
    finally:
        return g_proxy


def to_list(data):
    """
    将伪数组转为list
    :param data: key为0.1.2 的字典
    :return: list
    """
    if type(data) is list:
        return data
    result = [val for _, val in data.items()]

    return result


def datetime_offset_by_month(datetime1, n=1):
    # create a shortcut object for one day
    one_day = datetime.timedelta(days=1)

    # first use div and mod to determine year cycle
    q, r = divmod(datetime1.month + n, 12)

    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day

    '''
       if input date is the last day of this month
       then the output date should also be the last
       day of the target month, although the day
       www.iplaypy.com
       may be different.
       for example:
       datetime1 = 8.31
       datetime2 = 9.30
    '''

    if datetime1.month != (datetime1 + one_day).month:
        return datetime2

    '''
        if datetime1 day is bigger than last day of
        target month, then, use datetime2
        for example:
        datetime1 = 10.31
        datetime2 = 11.30
    '''

    if datetime1.day >= datetime2.day:
        return datetime2

    '''
     then, here, we just replace datetime2's day
     with the same of datetime1, that's ok.
    '''

    return datetime2.replace(day=datetime1.day)


def tran_bool(data):
    if data.lower() == str(True).lower():
        return True
    elif data.lower() == str(False).lower():
        return False
    return None


def date_format(dt: datetime=None, fmt='%Y-%m-%d'):
    if dt is None:
        return ''
    return dt.strftime(fmt)


def datetime_format(dt: datetime = None, fmt="%Y-%m-%d %H:%M:%S"):
    """
    时间格式化
    :param dt:
    :param fmt:
    :return:
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)