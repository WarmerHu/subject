#coding:utf-8
'''
Created on 2016年1月21日

@author: Warmer
'''
from subject.models import User, Topic
import time

'''
参数{"method":"-","column":"replyTime"}    method：+,-    column:time,replytime,modifytime
返回[{"id":12,"title":xx,"publisher":xx,"createTime":xx,"replyTime":xx,"modifyTime":xx},...]
'''
def select_topics_byReq(req):
    dao = Topic.objects.order_by(req["method"]+req["column"])
    rsp = []
    for v in dao:
        value = {}
        value["id"] = v.id
        value["title"] = v.name
        value["publisher"] = v.userid.username
        value["createTime"] = v.time
        value["replyTime"] = v.replytime
        value["modifyTime"] = v.modifytime
        rsp.append(value)
    return rsp

class BBSDao():
    def __init__(self,req):
        if req.has_key("username"):
            self.us = User.objects.get(username=req["username"])
    
    '''
    插入一则话题：
    1.获取当天时间
    2.判断用户当天已发布多少则话题：少于5，下一步；否则，返回false
                        判断当天：1.获取当前时间:%Y-%m-%d
                2.目标时间模糊查询
    3.插入话题至数据库
    '''
    def insert_a_topic(self,req):
        realtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if Topic.objects.filter(userid=self.us,time__startswith=realtime).count() < 5:
            realtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            Topic(userid=self.us,name=req["name"],content=req["content"],time=realtime,replytime=0,modifytime=realtime).save()
            return True
        return False
    
    def select_newestTopic_byUs(self):
        t = Topic.objects.filter(userid=self.us).order_by("-time")[:1]
        rsp = {}
        for v in t:
            rsp["id"] = v.id
        return rsp