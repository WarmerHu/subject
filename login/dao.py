#coding:utf-8
'''
Created on 2016-1-4
@author: 
description:
'''
from subject.models import User
def get_id_byName(req):
    e = User.objects.get(username=req)
    return e.id

def update_point_byReq(req):
    if req.has_key('username'):
        dao = User.objects.get(username=req['username'])
    elif req.has_key('id'):
        dao = User.objects.get(id=req['id'])
    if req['method'] == '+':
        dao.points += int(req['points'])
    else:
        dao.points -= int(req['points'])
    dao.save()
    return

def select_fortune():
    dao = User.objects.order_by("-points")
    rsp = []
    for v in dao:
        value = {}
        value["username"] = v.username
        value["head"] = v.head
        value["fortune"] = v.points
        rsp.append(value)
    return rsp
        