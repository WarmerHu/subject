#coding:utf-8
'''
Created on 2016年1月21日

@author: Warmer
'''
from subject.models import Topic, User, Opinion
from subject.globalData import ONE_PAGE_NUM, HOST_PORT
from django.utils import timezone
import time
from login.dao import userDao
from subject import settings


def select_Ctopic():
    return Topic.objects.count()

'''
参数{"method":"-","column":"replyTime"}    method：+,-    column:time,replytime,modifytime
返回[{"id":12,"title":xx,"publisher":xx,"createTime":xx,"replyTime":xx,"modifyTime":xx},...]
'''
def select_topics_byReq(req,page):
    dao = Topic.objects.order_by(req["method"]+req["column"])[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
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

class OpinDao:
    def __init__(self,req):
        if req.has_key("op"):
            self.op = req['op']
     
    def update_Ocomplaint(self,method):
        if method=='+':
            self.op.complaint += 1
        elif method=='-':
            self.op.complaint -= 1
        return self.op.complaint
      
    def update_state(self,req):
        self.op.state = req
      
    def update_save(self):
        self.op.save()

        

class BBSDao:
    def __init__(self,req):
        if req.has_key("username"):
            self.us = User.objects.get(username=req["username"])
        elif req.has_key("userid"):
            self.us = User.objects.get(id=req["userid"])
        if req.has_key("id"):
            self.bbs = Topic.objects.get(id=req["id"])
        elif req.has_key("bbs"):
            self.bbs = req["bbs"]
    
    def select_COBBS_by_us(self):
        q = '''select count(topicID) as num,topicID,opinion.id
            from opinion,topic where opinion.userID = '''+str(self.us.id)+''' and topicId=topic.id;'''
        o = Opinion.objects.raw(q)
        for v in o:
            return v.num
         
    def select_Obbs_by_us(self,page,each):
        q = '''select DISTINCT topicID,opinion.id, name,max(opinion.time) as newtime
            from opinion,topic where opinion.userID = '''+str(self.us.id)+''' and topicId=topic.id
            GROUP BY topicId order by newtime desc;'''
        opi = Opinion.objects.raw(q)[(page-1)*each:page*each]
        rsp = []
        for v in opi:
            value = {}
            value['topicId'] = v.topicID
            value['topicName'] = v.name
            value['time'] = timezone.localtime(v.newtime).strftime('%Y-%m-%d %H:%M:%S')
            rsp.append(value)
        print "rsp:",rsp
        return rsp
     
    def select_Cbbs_by_us(self):
        return  Topic.objects.filter(userid=self.us).count()
         
    def select_bbs_by_us(self,page,each):
        bbs = Topic.objects.filter(userid=self.us).order_by('-time')[(page-1)*each:page*each]
        rsp = []
        for v in bbs:
            value = {}
            value['topicId'] = v.id
            value['topicName'] = v.name
            value['time'] = timezone.localtime(v.time).strftime('%Y-%m-%d %H:%M:%S')
            rsp.append(value)
        return rsp
     
    def insert_a_opinion(self,req):
        realtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        if not Opinion.objects.filter(userid=self.us,topicid=self.bbs,time__startswith=realtime):
            realtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            Opinion(userid=self.us,topicid=self.bbs,opinion=req["content"],time=realtime,state='NORMAL',complaint=0).save()
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
         
    def update_Tcomplaint(self,method):
        if method=='+':
            self.bbs.complaint += 1
        elif method=='-':
            self.bbs.complaint -= 1
        return self.bbs.complaint
     
    def update_Tstate(self,req):
        self.bbs.state = req
     
    def update_Tsave(self):
        self.bbs.save()
     
    def select_topic(self, us=None):
        rsp = {}
        rsp["id"] = self.bbs.id
        rsp["topic"] = self.bbs.name
        rsp["content"] = self.bbs.content
        rsp["author"] = self.bbs.userid.username
        rsp["authorid"] = self.bbs.userid.id
        rsp["head"] = '/static/img/'+self.bbs.userid.head
        rsp["creatTime"] = timezone.localtime(self.bbs.time).strftime('%Y-%m-%d %H:%M:%S')
        rsp["replayTime"] = self.bbs.replytime
        from complaint.dao import complaintDao
        rsp['complaint'] = complaintDao({'topicid':rsp["id"], 'userid':us}).is_complaint_byTP()
#         rsp["opinions"] = self.select_opinions_byBBS()
        return rsp
     
    def select_Copinion_byBBS(self):
        return Opinion.objects.filter(topicid=self.bbs).count()
     
    def select_opinions_byBBS(self,page):
        dao = Opinion.objects.filter(topicid=self.bbs)[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
        rsp = []
        for v in dao:
            value = {}
            value["id"] = v.id
            value["name"] = v.userid.username
            value["authorid"] = v.userid.id
            value["head"] = '/static/img/'+v.userid.head
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
            Topic(userid=self.us,name=req["name"],content=req["content"],time=realtime,replytime=0,modifytime=realtime,state='NORMAL',complaint=0).save()
            return True
        return False
     
    def select_newestTopic_byUs(self):
        t = Topic.objects.filter(userid=self.us).order_by("-time")[:1]
        rsp = {}
        for v in t:
            rsp["id"] = v.id
            print rsp["id"]
        return rsp