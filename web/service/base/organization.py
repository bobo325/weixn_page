# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2018/1/9 14:24
"""
from datetime import datetime
from typing import List, Optional

from flask_app.app import db
from model.base.organization import Organization
from model.base.user import User
from util.oprlog import opr_data


def add(name, pid, enable, description, creator):
    org = Organization(
        name=name,
        pid=pid,
        enable=enable,
        description=description,
        creator=creator,
        create_time=datetime.now(),
        updator=creator,
        update_time=datetime.now()
    )
    opr_data(oid=creator, od={}, nd=org.to_dict())
    db.session.add(org)
    db.session.commit()


def update(org_id, updator, name=None, pid=None, description=None, enable=None):
    org = list_by_id(org_id)
    org.name = name if name is not None else org.name
    org.pid = pid if pid is not None else org.pid
    org.description = description if description is not None else org.description
    org.enable = enable if enable is not None else org.enable
    org.updator = updator
    org.update_time = datetime.now()
    db.session.add(org)
    new_org = list_by_id(org_id)
    opr_data(oid=updator, od=org.to_dict(), nd=new_org.to_dict())


def delete(ids, oid=0):
    for org_id in ids:
        sub_orgs_id = [x.id for x in list_all_sub_org(org_id)]
        if sub_orgs_id and len(User.query.filter(User.org_id.in_(sub_orgs_id)).all()) == 0:
            org = list_by_id(org_id)
            opr_data(oid=oid, od=org.to_dict(), nd={})
            db.session.delete(org)
        else:
            return False
    return True


def list_all_sub_org(org_id) -> List[Organization]:
    orgs = []
    org = list_by_id(org_id)
    # 排除没有
    if org is None:
        return []
    orgs.append(org)
    i = 0
    while i < len(orgs):
        sub_orgs = Organization.query.filter(Organization.pid == orgs[i].id).all()
        orgs += sub_orgs
        i += 1
    db.session.expunge_all()
    return orgs


def list_by_id(org_id) -> Optional[Organization]:
    org = Organization.query.filter(Organization.id == org_id).one_or_none()
    db.session.expunge_all()
    return org


def list_by_name(org_name) -> Optional[Organization]:
    org = Organization.query.filter(Organization.name == org_name).one_or_none()
    db.session.expunge_all()
    return org


def enable(ids: List[int], updator):
    for org_id in ids:
        for need_org in list_all_sub_org(org_id):
            update(need_org.id, updator, enable=True)


def disable(ids: List[int], updator):
    for org_id in ids:
        for need_org in list_all_sub_org(org_id):
            update(need_org.id, updator, enable=False)
