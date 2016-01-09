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

def update_point_byName(req):
    dao = User.objects.get(username=req)
    dao.points += 1
    dao.save()
    return    
