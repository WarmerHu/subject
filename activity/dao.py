#coding:utf-8
'''
Created on 2016-1-4
@author: 
description:
'''
from subject.models import Activity, User
import time

class activityDao():
    def __init__(self,req):
        self.us = User.objects.get(id=req)

    def add_a_activity(self,realcontent):
        realtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        Activity(userid=self.us,content=realcontent,time=realtime).save()
        return
