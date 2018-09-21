#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 17:22
"""
import json

from flask_app import app
from util.common import get_g
from util.log_builder import logging


@app.after_request
def response_handler(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,token,captcha-id'
    response.headers['Access-Control-Expose-Headers'] = 'captcha-id'
    if response.headers['Content-Type'] == "application/json":
        data = json.loads(response.data.decode())
        if data['code'] != 0:
            g = get_g()
            g.opr_fail = True
    logging.info("response is [{}]".format(response.data.decode()))
    return response
