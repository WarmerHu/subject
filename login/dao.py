#coding:utf-8
'''
Created on 2016-1-4
@author: 
description:
'''
from subject.models import User
from subject import settings
from subject.globalData import ONE_PAGE_NUM

def select_Cuser():
    return User.objects.count()

def select_fortune(page):
    dao = User.objects.order_by("-points")[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
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
    name = ''
    def __init__(self,req):
        if req.has_key('userid'):
            self.us = User.objects.get(id=req['userid'])
        elif req.has_key('username'):
            self.us = User.objects.get(username=req['username'])
        elif req.has_key('email'):
            self.us = User.objects.get(email=req['email'])
            self.name = self.us.username
    
    def update_state(self,req):
        self.us.state = req
        
    def update_point_byReq(self,req):
        if req['method'] == '+':
            self.us.points += int(req['points'])
        else:
            self.us.points -= int(req['points'])
            self.us.save()
    
    def update_flag(self,req):
        self.us.flag = req
        
    def update_ps(self,req):
        self.us.password = req
    
    def update_head(self,req):
        self.us.head = req
    
    def save_update(self):
        self.us.save()
        
    def select_user(self):
        rsp = {}
        rsp['head'] = settings.STATIC_URL+'img/'+self.us.head
        rsp['name'] = self.us.username
        rsp['email'] = self.us.email
        rsp['point'] = self.us.points
        return rsp 
    
def uploadHead(req):
    f_path = settings.STATIC_ROOT + req['filename']
    with open(f_path,'wb+') as info:
        for chunk in req['file'].chunks():
            info.write(chunk)
    dao = userDao({"userid":req['userid']})
    dao.update_head(req['filename'])
    dao.save_update()
    
    