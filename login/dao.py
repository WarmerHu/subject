#coding:utf-8
'''
Created on 2016-1-4
@author: 
description:
'''
from subject.models import User

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

class userDao():
    us = ''
    def __init__(self,req):
        if req.has_key('userid'):
            self.us = User.objects.get(id=req['userid'])
        elif req.has_key('username'):
            self.us = User.objects.get(username=req['username'])
    
    def update_state(self):
        self.us.state = 'NORMAL'
        self.us.save()
        
    def update_point_byReq(self,req):
        if req['method'] == '+':
            self.us.points += int(req['points'])
        else:
            self.us.points -= int(req['points'])
            self.us.save()
    
    def update_flag(self,req):
        self.us.flag = req
        self.us.save()
    
    