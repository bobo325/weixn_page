# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2018-01-08 15:51
"""
import os

"""
环境开关   prod  test  local
"""
config = str(os.getenv("CONFIG", 'dev')).strip()

if config == "prod":
    from config.prod import *
elif config == "test":
    from config.test import *
else:
    from config.dev import *
