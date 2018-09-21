# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: arcr@163.com
@time: 2018-05-22 9:01
"""
from celery import Celery, platforms

celery_app = Celery('chtnew_manager')
celery_app.config_from_object('proj.celeryconfig')
platforms.C_FORCE_ROOT = True
celery_app.task()