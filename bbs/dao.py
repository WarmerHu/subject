#coding:utf-8
'''
Created on 2016年1月21日

@author: Warmer
'''
from subject.models import User, Topic, Opinion
import time
import datetime
from subject import settings
from django.utils import timezone
from login.dao import userDao

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
        value["createTime"] = timezone.localtime(v.time).strftime('%Y-%m-%d %H:%M:%S')
        value["replyTime"] = v.replytime
        value["modifyTime"] = timezone.localtime(v.modifytime).strftime('%Y-%m-%d %H:%M:%S')
        rsp.append(value)
    return rsp


        

class BBSDao():
    def __init__(self,req):
        if req.has_key("username"):
            self.us = User.objects.get(username=req["username"])
        elif req.has_key("userid"):
            self.us = User.objects.get(id=req["userid"])
        if req.has_key("id"):
            self.bbs = Topic.objects.get(id=req["id"])
    
    def insert_a_opinion(self,req):
        realtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        if not Opinion.objects.filter(userid=self.us,topicid=self.bbs,time__startswith=realtime):
            realtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            Opinion(userid=self.us,topicid=self.bbs,opinion=req["content"],time=realtime).save()
            self.update_topic({"realtime":realtime})
            userDao({'userid':req['userid']}).update_point_byReq({'method':'+','points':1})
            num = Opinion.objects.filter(topicid=self.bbs).count()
            if not num%5:
                userDao({'userid':self.bbs.userid.id}).update_point_byReq({'method':'+','points':num/5})
            return True
        return False
    
    def update_topic(self,req):
        self.bbs.replytime += 1
        if req.has_key("realtime"):
            self.bbs.modifytime = req["realtime"]
        self.bbs.save()
    
    def select_topicOpinions(self):
        rsp = {}
        rsp["id"] = self.bbs.id
        rsp["topic"] = self.bbs.name
        rsp["content"] = self.bbs.content
        rsp["author"] = self.bbs.userid.username
        rsp["head"] = settings.STATIC_URL+'img/'+self.bbs.userid.head
        rsp["creatTime"] = timezone.localtime(self.bbs.time).strftime('%Y-%m-%d %H:%M:%S')
        rsp["replayTime"] = self.bbs.replytime
        rsp["opinions"] = self.select_opinions_byBBS()
        return rsp
    
    def select_opinions_byBBS(self):
        dao = Opinion.objects.filter(topicid=self.bbs)
        rsp = []
        for v in dao:
            value = {}
            value["id"] = v.id
            value["name"] = v.userid.username
            value["head"] = settings.STATIC_URL+'img/'+v.userid.head
            value["content"] = v.opinion
            value["time"] = timezone.localtime(v.time).strftime('%Y-%m-%d %H:%M:%S')
            rsp.append(value)
        return rsp
    
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
            print rsp["id"]
        return rsp