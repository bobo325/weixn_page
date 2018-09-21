#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 13:32
"""
from flask_app import app
from service.base.opration_record import opr_entry


@app.teardown_request
def opr_entry_fulfill(exception):
    success, _ = opr_entry()