#coding:utf-8
'''
Created on 2016-1-4
@author: 
description:
'''
from subject.models import Activity, User
import time
import datetime


def select_activity(req):
    dao = Activity.objects.order_by("-id")[:req]
    rsp = []
    for v in dao:
        rsp.append('\t'.join([datetime.datetime.strftime(v.time,'%Y-%m-%d %H:%M:%S'), v.content]))
    return rsp

class activityDao():
    def __init__(self,req):
        if req.has_key("id"):
            self.us = User.objects.get(id=req["id"])
        elif req.has_key("username"):
            self.us = User.objects.get(username=req["username"])

    def add_a_activity(self,realcontent):
        realtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        Activity(userid=self.us,content=realcontent,time=realtime).save()
        return
