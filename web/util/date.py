#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime


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