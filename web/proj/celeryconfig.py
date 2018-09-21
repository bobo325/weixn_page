# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: arcr@163.com
@time: 2018-02-08 11:44
"""
# Broker and Backend
from datetime import timedelta

from celery.schedules import crontab

from config import pgsql_pool_configs, task_config

broker_url = task_config['rabbit_mq_url']
result_backend = pgsql_pool_configs['url'].replace("postgresql+psycopg2", "db+postgresql")

enable_utc = True

timezone = 'UTC'

task_serializer = 'json'

result_serializer = 'json'

accept_content = ['json']

# import
imports = (
    'proj.tasks'
)

# beat_schedule = {
#     'sched_close_order': {
#         'task': 'proj.tasks.sched_shop_statistics',
#         'schedule': crontab(hour=task_config['member_statistics_cron'][0],
#                             minute=task_config['member_statistics_cron'][1]),  # 北京时间00:15:00
#         'args': (),
#     },
# }
