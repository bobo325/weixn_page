#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2018/1/9 11:22
"""
from flask import Flask
from flask_redis import Redis
from flask_sqlalchemy import SQLAlchemy

from config import pgsql_pool_configs, redis_config

app = Flask(__name__)

# setup redis
app.config['REDIS_URL'] = redis_config["url"]
redis = Redis(app)

# setup SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = pgsql_pool_configs['url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
