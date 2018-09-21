# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/9 14:12
"""

from flask import request

from const import msg
from flask_app import app
from service.base import organization
from service.base.organization import list_by_name
from util.common import build_ret, to_list, get_g


@app.route("/org/add", methods=["POST"])
def org_add():
    current_user = get_g().user
    args = request.json

    if list_by_name(args["name"]):
        return build_ret(msg.SYS_NAME_REPEATED_ERR)

    organization.add(
        name=args["name"],
        pid=args.get("pid", 1),
        enable=True,
        description=args['description'],
        creator=current_user.id
    )
    return build_ret(msg.SYS_SUCCESS)


@app.route("/org/update", methods=["POST"])
def org_update():
    current_user = get_g().user
    args = request.json
    organization.update(
        org_id=args['id'],
        updator=current_user.id,
        name=args["name"],
        pid=args.get("pid", 0 if args['id'] == 1 else 1),
        description=args['description']
    )
    return build_ret(msg.SYS_SUCCESS)


@app.route("/org/delete", methods=["POST"])
def org_delete():
    current_user = get_g().user
    res = organization.delete(
        ids=to_list(request.json['id']), oid=current_user.id
    )
    if res:
        return build_ret(msg.SYS_SUCCESS)
    else:
        return build_ret(msg.ORGANIZATION_DELETE_ERROR)


@app.route("/org/list", methods=["GET"])
def org_list():
    current_user = get_g().user
    data = [x.to_dict() for x in organization.list_all_sub_org(current_user.org_id)]
    return build_ret(msg.SYS_SUCCESS, total=len(data), data=data)


# @app.route("/org/enable", methods=["POST"])
def org_enable():
    current_user = get_g().user
    organization.enable(
        ids=to_list(request.json),
        updator=current_user.id
    )
    return build_ret(msg.SYS_SUCCESS)


# @app.route("/org/disable", methods=["POST"])
def org_disable():
    current_user = get_g().user
    organization.disable(
        ids=to_list(request.json),
        updator=current_user.id
    )
    return build_ret(msg.SYS_SUCCESS)
