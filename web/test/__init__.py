# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/9 17:03
"""
from unittest import mock

from redis import StrictRedis
from sqlalchemy import BigInteger
from sqlalchemy.ext.compiler import compiles

from flask_app import app


# sqlite 类型适配
# BigIntegerType = sqlalchemy.BigInteger()
# BigIntegerType.with_variant(sqlite.INTEGER(), 'sqlite')
# sqlalchemy.BigInteger = BigIntegerType
# web["init_sql_path"] = "../sql/pgsql_init_data.sql"

@compiles(BigInteger, 'sqlite')
def bi_c(element, compiler, **kw):
    return "INTEGER"


@compiles(BigInteger)
def bi_c(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)


class BigInteger(BigInteger):
    pass


# DB Mock
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

# Redis Mock
redis_map = {}
order_id = [str(i).encode() for i in range(10000000000, 10000001000)]


def get(key):
    global redis_map
    return redis_map.get(key, None)


def set(key, value, **kwargs):
    global redis_map
    if isinstance(value, str):
        redis_map[key] = value.encode()
    else:
        redis_map[key] = value


def lpop(key):
    global order_id
    return order_id.pop()


def delete(key):
    global redis_map
    redis_map.pop(key)


redis_mock = mock.MagicMock(spec=StrictRedis)

redis_mock.get = get
redis_mock.set = set
redis_mock.lpop = lpop
redis_mock.delete = delete
app.extensions['redis']['REDIS'] = redis_mock = redis_mock

# 发短信模块Mock
SMS_SENT_CONTENT = None


def sms_send(phone, code):
    global SMS_SENT_CONTENT
    SMS_SENT_CONTENT = {
        "phone": phone,
        "code": code
    }
    return True


def get_sent_sms():
    return SMS_SENT_CONTENT


# sms_aliyun.sms_send = sms_send

# 创表
# db.create_all()

test_client = app.test_client()
