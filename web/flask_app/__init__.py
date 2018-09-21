#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2018/1/9 11:22
"""

from flask_app.app import app, redis, db
from flask_app.error_handle import *
from util.file import package_import

package_import("route")
package_import("intercept")
