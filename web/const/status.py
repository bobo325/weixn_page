# /usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: ChenBo
@contact: 1126531273@qq.com
@time: 2018/07/17 10:00
"""

from enum import IntEnum


class AuthTypeEnum(IntEnum):
    # 手机号验证
    PHONE = 1
    # 微信验证
    WEIXIN = 2

