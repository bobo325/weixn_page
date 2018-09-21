#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2018/02/26 14:00
"""
from flask_app import app
from util.log_builder import logging
from config import web
from flask_app.app import db


@app.before_first_request
def first_request():
    # 创建表
    # db.create_all()
    logging.info("template before first request: postgres init table")
    # 初始化数据
    file = open(web['init_sql_path'], encoding="utf-8")
    sql = ""  # 拼接的sql语句
    for each_line in file.readlines():
        if not each_line or each_line == "\n" or each_line[0:2] == '--':
            continue
        else:
            sql += each_line
    if sql:
        sqls = sql.split(";")
        for s in sqls:
            if s:
                try:
                    db.session.execute(s)
                    db.session.commit()
                except Exception as e:
                    logging.error(e)
                    db.session.rollback()
    file.close()
