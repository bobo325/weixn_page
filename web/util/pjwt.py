#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/10/13 9:43
"""
import random
import string
import time

import jwt

from config import ex_time, jwt_cnf
from flask_app.app import redis


def en_token(id, username, org_id, org_name, role_id, role_name):
    iat = time.time()
    exp = iat + ex_time['token_ex']
    payload = {
        'username': str(username),
        'id': str(id),
        'org_id': str(org_id),
        'org_name': org_name,
        'role_id': str(role_id),
        'role_name': role_name,
        'iat': iat,
        'exp': exp
    }
    key_pix = generate_key()
    token = jwt.encode(payload, jwt_cnf['token_key'] + key_pix, algorithm='HS256')
    redis.connection.set(token, key_pix)
    return token


def de_token(token):
    if token is None:
        return None
    token = str(token)
    token_key_pix = redis.connection.get(token)
    if token_key_pix is None:
        return None
    token_key_pix = token_key_pix.decode()
    token_keys = jwt_cnf['token_key'] + token_key_pix
    no_valid_token = jwt.decode(token, token_keys, algorithms=['HS256'])
    return no_valid_token


def generate_key():
    """
    生成秘钥字符串
    :return: 
    """
    base_str = string.digits + string.ascii_letters
    key_list = [random.choice(base_str) for i in range(jwt_cnf['key_len'])]
    key_str = "".join(key_list)
    return key_str
