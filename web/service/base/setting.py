#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/9 10:30
"""
from const import msg
from flask_app.app import db
from model import Metadata
from util.oprlog import opr_data


def system_setting(name: str, company: str, version: str, logo: str, favicon: str, oid: int):
    system = Metadata.query.filter(Metadata.id == 1).one_or_none()
    if not system:
        new_system = Metadata(name=name, version=version, company=company, favicon=favicon, logo=logo)
        db.session.add(new_system)
        od = {}
    else:
        od = system.to_json()
        system.name = name
        system.company = company
        system.version = version
        system.logo = logo
        system.favicon = favicon
    db.session.commit()
    new_data = Metadata.query.filter(Metadata.id == 1).one_or_none()
    nd = new_data.to_json()
    opr_data(oid=oid, od=od, nd=nd)
    return True, msg.SYS_SUCCESS


def login_setting(lut: int, ct: bool, oid: int):
    system = Metadata.query.get(1)
    if not system:
        new_system = Metadata(lut=lut, ct=ct)
        db.session.add(new_system)
        od = {}
    else:
        od = system.to_json()
        system.lock_user_threshold = lut
        system.captcha_threshold = ct
    db.session.commit()
    new_data = Metadata.query.get(1)
    nd = new_data.to_json()
    opr_data(oid=oid, od=od, nd=nd)
    return True, msg.SYS_SUCCESS


def system_list():
    system = Metadata.query.filter(Metadata.id == 1).one_or_none()
    if not system:
        data = {
            "name": "",
            "version": "",
            "company": "",
            "logo": "",
            "favicon": "",
            "lock_user_threshold": 0,
            "captcha_threshold": False
        }
    else:
        data = system.to_json()
    return True, data
