#coding:utf-8
'''
Created on 2016年4月17日

@author: warmer
'''
from subject.models import User, Exercise, Complaint, Topic, Opinion, Source
from login.dao import userDao
from resources.dao import rsUpdateDao
from django.db.models.query_utils import Q
from subject.globalData import ONE_PAGE_NUM

class complaintDao:
    def __init__(self,req):
        self.us = None
        self.ex = None
        self.au = None
        self.tp = None
        self.op = None
        self.rs = None
        if req.has_key('userid'):
            uss = req['userid']
            if uss:
                self.us = User.objects.get(id=uss)
        if req.has_key('titleid'):
            self.ex = Exercise.objects.get(id=req['titleid'])
        if req.has_key('authorid'):
            self.au = User.objects.get(id=req['authorid'])
        if req.has_key('topicid'):
            self.tp = Topic.objects.get(id=req['topicid'])
        if req.has_key('opinionid'):
            self.op = Opinion.objects.get(id=req['opinionid'])
        if req.has_key("rsid"):
            self.rs = Source.objects.get(id=req["rsid"])
    
    def select_complaint_byUS(self,page):
        rs_alll = Complaint.objects.filter(userid=self.us,state="NORMAL")
        result = {}
        if page==0:
            result['numT'] = rs_alll.count()
            page = 1
        rs_all = rs_alll[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
        rs = []
        for v in rs_all:
            rsp = {}
            rsp["content"] = v.content
            if v.titleid:
                rsp["titleid"] = v.titleid.id 
                rsp["titlename"] = v.titleid.title
                rsp["titleauid"] = v.titleid.userid.id
                rsp["titleauname"] = v.titleid.userid.username
            if v.resourceid:
                rsp["rsid"] = v.resourceid.id 
                rsp["rsname"] = v.resourceid.download
                rsp["rsauid"] = v.resourceid.userid.id
                rsp["rsauname"] = v.resourceid.userid.username
            if v.topicid:
                rsp["tpid"] = v.topicid.id 
                rsp["tpname"] = v.topicid.name
                rsp["tpauid"] = v.topicid.userid.id
                rsp["tpauname"] = v.topicid.userid.username
            if v.opinionid:
                rsp["opid"] = v.opinionid.id 
                rsp["opname"] = v.opinionid.opinion
                rsp["optpid"] = v.opinionid.topicid.id
                rsp["optpname"] = v.opinionid.topicid.name
                rsp["opauid"] = v.opinionid.userid.id
                rsp["opauname"] = v.opinionid.userid.username
            if v.authorid:
                rsp["auid"] = v.authorid.id 
                rsp["auname"] = v.authorid.username
            rs.append(rsp)
        result['result'] = rs
        return result
    
    def select_complaint_byAU(self,page):
        exx = Exercise.objects.filter(userid=self.au)
        rss = Source.objects.filter(userid=self.au)
        tpp = Topic.objects.filter(userid=self.au)
        opp = Opinion.objects.filter(userid=self.au)
        rs_alll = Complaint.objects.filter((Q(authorid=self.au) | Q(titleid__in=exx) | Q(resourceid__in=rss) | Q(topicid__in=tpp) | Q(opinionid__in=opp)), Q(state="NORMAL"))
        result = {}
        if page==0:
            result['numT'] = rs_alll.count()
            page = 1
        rs_all = rs_alll[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
        rs = []
        for v in rs_all:
            rsp = {}
            rsp["fromid"] = v.userid.id
            rsp["fromname"] = v.userid.username
            rsp["fromemail"] = v.userid.email
            rsp["content"] = v.content
            if v.titleid:
                rsp["titleid"] = v.titleid.id 
                rsp["titlename"] = v.titleid.title
            if v.resourceid:
                rsp["rsid"] = v.resourceid.id 
                rsp["rsname"] = v.resourceid.download
            if v.topicid:
                rsp["tpid"] = v.topicid.id 
                rsp["tpname"] = v.topicid.name
            if v.opinionid:
                rsp["opid"] = v.opinionid.id 
                rsp["opname"] = v.opinionid.opinion
                rsp["optpid"] = v.opinionid.topicid.id
                rsp["optpname"] = v.opinionid.topicid.name
            if v.authorid:
                rsp["auid"] = v.authorid.id 
                rsp["auname"] = v.authorid.username
            rs.append(rsp)
        result['result'] = rs
        return result
    
    def is_complaint_byEX(self):
        if  Complaint.objects.filter(titleid=self.ex, userid=self.us, state='NORMAL'):
            return True
        return False
            
    def is_complaint_byTP(self):
        if  self.us:
            if Complaint.objects.filter(topicid=self.tp, userid=self.us, state='NORMAL'):
                return True
        return False
    
    def is_complaint_byOP(self):
        if  self.us:
            if Complaint.objects.filter(opinionid=self.op, userid=self.us, state='NORMAL'):
                return True
        return False

    def is_complaint_byAU(self):
        if  Complaint.objects.filter(userid=self.us, authorid=self.au, state='NORMAL'):
            return True
        return False
    
    def is_complaint_byRS(self):
        if  Complaint.objects.filter(userid=self.us, resourceid=self.rs, state='NORMAL'):
            return True
        return False
    
    def insert_a_complaint(self,req):
        if self.ex:
            n =  Complaint.objects.filter(titleid=self.ex).count()
            if n<5:
                Complaint(titleid=self.ex, content=req['content'],userid=self.us, state='NORMAL').save()
                from exercise.dao import updateEXDao
                dao = updateEXDao() 
                if dao.update_exercise_complaint( method='+',ex=self.ex)==5:
                    dao.update_exercise_state('ACTIVE', self.ex)
                    dao.update_ex_save()
                return 'complain successfully'
        elif self.au:
            n =  Complaint.objects.filter( authorid=self.au).count()
            if n<10:
                Complaint(authorid=self.au, content=req['content'],userid=self.us, state='NORMAL').save()
                dao = userDao({'us':self.au})
                if dao.update_complaint('+')==10:
                    dao.update_state('ACTIVE')
                    dao.save_update()
                return None
        elif self.tp:
            n =  Complaint.objects.filter( topicid=self.tp).count()
            if n<10:
                Complaint(topicid=self.tp, content=req['content'],userid=self.us, state='NORMAL').save()
                from bbs.dao import BBSDao
                dao = BBSDao({'bbs':self.tp})
                if dao.update_Tcomplaint('+')==10:
                    dao.update_Tstate('ACTIVE')
                    dao.update_Tsave()
                return None
        elif self.op:
            n =  Complaint.objects.filter(opinionid=self.op).count()
            if n<5:
                Complaint(opinionid=self.op, content=req['content'],userid=self.us, state='NORMAL').save()
                from bbs.dao import OpinDao
                dao = OpinDao({'op':self.op})
                if dao.update_Ocomplaint('+')==10:
                    dao.update_state('ACTIVE')
                    dao.save_update()
                return None
        elif self.rs:
            n =  Complaint.objects.filter(resourceid=self.rs).count()
            if n<10:
                Complaint(resourceid=self.rs, content=req['content'],userid=self.us, state='NORMAL').save()
                dao = rsUpdateDao(self.rs)
                n = dao.update_complaint('+')
                if dao.update_complaint('+')==10:
                    dao.update_state('ACTIVE')
                    dao.update_save()
                return None
        return 'wrong request'        
        
    def update_a_complaint(self,key,method):
        if self.ex:
            cm = Complaint.objects.get(titleid=self.ex, userid=self.us,state="NORMAL")
            from exercise.dao import updateEXDao
            dao = updateEXDao()
            dao.update_exercise_complaint( method ,ex=self.ex)
            dao.update_ex_save()
        elif self.au:
            cm = Complaint.objects.get(authorid=self.au, userid=self.us,state="NORMAL")
            dao = userDao({'us':self.au})
            dao.update_complaint(method)
            dao.save_update()
        elif self.tp:
            cm = Complaint.objects.get(topicid=self.tp, userid=self.us,state="NORMAL")
            from bbs.dao import BBSDao
            dao = BBSDao({'bbs':self.tp})
            dao.update_Tcomplaint(method)
            dao.update_Tsave()
        elif self.op:
            cm = Complaint.objects.get(opinionid=self.op, userid=self.us,state="NORMAL")
            from bbs.dao import OpinDao
            dao = OpinDao({'op':self.op})
            dao.update_Ocomplaint(method)
            dao.update_save()
        elif self.rs:
            cm = Complaint.objects.get(resourceid=self.rs, userid=self.us,state="NORMAL")
            dao = rsUpdateDao(self.rs)
            dao.update_complaint(method)
            dao.update_save()
        if key=='state':
            cm.state = 'CANCEL'
        cm.save()
            
            
