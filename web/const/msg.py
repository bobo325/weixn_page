#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 9:39
"""


class Code:
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


# common
SYS_SUCCESS = Code(code=0, msg=u"操作成功")
SYS_FAIL = Code(code=1, msg=u"操作失败")

# common error
SYS_RECORD_NOT_FOUND = Code(code=9991, msg=u"记录不存在")
SYS_NAME_REPEATED_ERR = Code(code=9992, msg=u"名称重复")
SYS_INVALID_REQUEST = Code(code=9993, msg="错误的请求")
SYS_NOT_FOUND = Code(code=9994, msg="页面不存在")
CODE_SYS_ERROR = Code(9995, "系统错误")
CODE_VALIDATE_ERROR = Code(9996, "数据验证错误")

# user model(10001-10050)
A_MAX_REQUEST = Code(10001, u"请求频繁，稍后再试")
A_SMS_ERR = Code(10002, u"请求频繁，稍后再试")
A_CODE_ERR = Code(10003, u"验证码错误")
A_CODE_TIMEOUT = Code(10004, u"验证码已失效")
USER_OLD_PWD_ERR = Code(code=10005, msg=u"用户原密码不正确")
USER_PWD_ERR = Code(10005, u"用户名或密码不正确")
USER_ORG_DISABLE = Code(10006, u"用户所在组织架构已删除或已禁用")
USER_ROLE_DISABLE = Code(10007, u"用户所在角色已删除或已禁用")
A_NO_AUTHOR = Code(10008, u"权限不足")
A_TIMEOUT = Code(10009, u"登录失效")
A_SIGNED = Code(10010, u"账号已在其他地方登录")
USER_EXISTS = Code(10011, u"账号已存在")
USER_DISABLE = Code(10012, u"该用户帐号已被禁用，请联系管理员")
USER_LOCKED = Code(10012, u"该用户帐号已被锁定，请联系管理员")

# message(11001)
MESSAGE_UN_RECORD = Code(code=11001, msg=u"系统不存在接收者记录")
MESSAGE_DEL = Code(code=11002, msg=u"消息已被删除")
MESSAGE_READ = Code(code=11003, msg=u"消息已被标记")

# organization
ORGANIZATION_DELETE_ERROR = Code(13001, u"该组织下仍存在用户，不能删除！")

# media model(12001-12050)
FILE_FORMAT_ERR = Code(code=12001, msg=u"文件格式错误")

