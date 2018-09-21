#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/10/13 11:40
"""
import base64
from io import BytesIO

from flask import send_file, make_response

from config import ex_time, r_pre
from const import msg
from flask_app import app
from flask_app.app import redis as redis_service
from util.captcha import create_validate_code
from util.common import get_uuid, build_ret


@app.route("/system_base/captcha", methods=['GET'])
def system_base_captcha():
    """
    获取验证码
    :return:
    """
    code_image, code_num = create_validate_code()
    byte_io = BytesIO()
    code_image.save(byte_io, 'PNG')
    pic_str = base64.b64encode(byte_io.getvalue()).decode()

    captcha_id = get_uuid()
    redis_service.set(r_pre['user_captcha'] + captcha_id, code_num, ex=ex_time['captcha_ex'])
    data = [dict(
        captcha_id=captcha_id,
        captcha=pic_str
    )]
    response = make_response(send_file(byte_io, mimetype='image/png', cache_timeout=0))
    response.headers['captcha_id'] = captcha_id
    return build_ret(msg.SYS_SUCCESS, data=data)
