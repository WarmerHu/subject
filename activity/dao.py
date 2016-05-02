#coding:utf-8
'''
Created on 2016-1-4
@author: 
description:
'''
from subject.models import Activity, User
import time
from django.utils import timezone


def select_activity(req):
    dao = Activity.objects.order_by("-id")[:req]
    rsp = []
    for v in dao:
        rsp.append('\t'.join([timezone.localtime(v.time).strftime('%Y-%m-%d %H:%M:%S'), v.content]))
    return rsp

def is_activity(req):
    if Activity.objects.filter(content=req):
        return True
    return False

class activityDao():
    def __init__(self,req):
        if req.has_key("userid"):
            self.us = User.objects.get(id=req["userid"])

    def add_a_activity(self,realcontent):
        realtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        Activity(userid=self.us,content=self.us.username.encode('utf-8')+realcontent,time=realtime).save()
        return
    
    