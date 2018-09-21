# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/10 17:24
"""

"""
一些单元测试中会使用到的常量
"""

"""
这个KEY在运行单元测试时需要设置到app.config中
用来区分单元测试环境和正式环境
因为单元测试环境可能会有一些地方需要被跳过，例如：登陆校验

:示例
app.config[TESTING_CONFIG_KEY] = True
"""
TESTING_CONFIG_KEY = 'TEST'
