#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/10/10 15:56
"""
import os

PROJECT_NAME = os.getenv("PROJECT_NAME", 'template')
SYSLOG_HOST = os.getenv('SYSLOG_HOST', '10.10.0.63')
SYSLOG_PORT = int(os.getenv('SYSLOG_PORT', 12201))
SYSLOG_LEVEL = os.getenv('SYSLOG_LEVEL', 'DEBUG')

# web
web = {
    "url_pre": "/api/%s/admin" % PROJECT_NAME,
    "api_version": ["v1"],
    "ip": "0.0.0.0",
    "port": 8080,
    "debug": True,
    "root": True,
    "token_key": "youLuKeJi",
    "key_len": 8,
    "pic_pix": "/static_file/",
    "pic_read": "/data/www",
    "init_sql_path": "/data/sql/pgsql_init_data.sql",  # 初始化sql数据脚本绝对路径
    "static_avatar": "/static_file/resources/pic/default-avatar.png",
}

pgsql_pool_configs = {
    "url": "postgresql+psycopg2://%s:youlu_dc_666666@pgsql:5432/%s" % (PROJECT_NAME, PROJECT_NAME),
    "pool_size": 1,
    "max_overflow": 10,
    "pool_recycle": 2 * 60 * 60

}

# redis配置
redis_config = {
    "url": "redis://redis:6379/0"
}

# 日志配置
log = {
    "name": "%s_web_v1" % PROJECT_NAME,
    "level": SYSLOG_LEVEL,
    "console": False,
    "format": "%(thread)d:%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s",
    "file": {
        "enable": False,
        "path": ""
    },
    "syslog": {
        "enable": False,
        "ip": "127.0.0.1",
        "port": 10514,
        "facility": "local5"
    },
    "gelf": {
        "enable": True,
        "ip": SYSLOG_HOST,
        "port": SYSLOG_PORT,
        "debug": True,
        "tag": PROJECT_NAME
    }

}

# redis有效时间配置
ex_time = {
    'captcha_ex': 2 * 60,
    'session_ex': 30 * 60,
    'token_ex': 10 * 24 * 60 * 60
}

# redis 各模块存储前缀
r_pre = {
    # 验证码
    "user_captcha": "tmp:u_c_",
    # 用户密码输入错误次数统计（email -> counts）
    "user_pwd_err_nums": "tmp:u_p_n_",
    "login_err_nums": 5,
    "token_pre": "tmp:u_t_"
}

# jwt配置
jwt_cnf = {
    "key_len": 8,
    "token_key": "tmp:tk_"
}

task_config = {
    "rabbit_mq_url": 'amqp://guest:guest@rabbitmq:5672//'
}