# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: arcr@163.com
@time: 2018-02-08 11:44
"""
from proj import celery_app as app
from util.log_builder import logging


class Tasks(app.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error('task exec fail, task_id: %s,\n , args: %s, error:' % (task_id, args), exc_info=1)


####################################
####################################
####################################
# schedule tasks


@app.task(base=Tasks)
def sched_shop_statistics():
    """
    定时扫描，关闭待支付订单（主要用于补偿APP那边没有传过来的订单）
    :return:
    """
    pass
    # logging.info("cht begin sched_shop_statistics...")
    # try:
    #     # service.order.sched_close_no_pay_order()
    #     service.shop.member_statistics()
    # except Exception as exc:
    #     logging.error("cht sched_shop_statistics error:", exc, exc_info=1)
    #     # raise self.retry(exc=exc, countdown=30, max_retries=3)
    # logging.info("cht end sched_shop_statistics")


####################################
####################################
####################################
# real time tasks


# @app.task(base=Tasks, bind=True)
# def close_no_pay_order(self, order_no):
#     """
#     超时关闭待支付订单
#     :return:
#     """
#     logging.info("chtnew begin close_no_pay_order_job..., order_no: %s" % order_no)
#     try:
#         pass
#     except Exception as exc:
#         logging.error("chtnew close_no_pay_order_job error:", exc, exc_info=1)
#         # overrides the default delay to retry after 1 minute
#         raise self.retry(exc=exc, countdown=30, max_retries=3)
#     logging.info("chtnew end close_no_pay_order_job...")
#
