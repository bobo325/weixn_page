#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 11:36
"""
from util.common import get_g


def opr_data(oid: int, nd: dict, od: dict):
    """
    操作日志新旧数据收集，该函数必须在请求上下文下调用，否则将会发生异常   
    :param nd:  改动后的新数据
    :param od:  改动前的旧数据
    :return: Boolean, True or False
    """
    g = get_g()
    g.nd = nd
    g.od = od
    g.oid = oid
    return True
