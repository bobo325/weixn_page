# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/10 10:29
"""
import json
from urllib.parse import urlencode

from flask import Response


def get(client, url: str, data=None, headers: dict = None):
    """
    发送GET请求
    data参数会自动转化成query string
    :param client: 测试客户端
    :param url:
    :param data:
    :param headers:
    :return:
    """
    if data:
        url += "?%s" % urlencode(data)
    resp = client.get(url, headers=headers)
    return get_data(resp)


def post(client, url: str, data=None, headers: dict = None):
    """
    发送POST请求
    :param client:
    :param url:
    :param data:
    :param headers:
    :return:
    """
    try:
        data = json.dumps(data)
    except:
        pass

    resp = client.post(url, data=data, headers=headers)
    return get_data(resp)


def get_data(response: Response) -> dict:
    return json.loads(response.data.decode())
