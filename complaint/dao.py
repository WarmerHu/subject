#coding:utf-8
'''
Created on 2016年4月17日

@author: warmer
'''
from subject.models import User, Exercise, Complaint, Topic, Opinion
from login.dao import userDao


class complaintDao:
    def __init__(self,req):
        self.us = None
        self.ex = None
        self.au = None
        self.tp = None
        self.op = None
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
        return 'wrong request'        
        
    def update_a_complaint(self,key,obj,method):
        if obj=='titleid':
            cm = Complaint.objects.get(titleid=self.ex, userid=self.us)
            from exercise.dao import updateEXDao
            dao = updateEXDao()
            dao.update_exercise_complaint( method ,ex=self.ex)
            dao.update_ex_save()
        elif obj=='authorid':
            cm = Complaint.objects.get(authorid=self.au, userid=self.us)
            dao = userDao({'us':self.au})
            dao.update_complaint(method)
            dao.save_update()
        elif self.tp:
            cm = Complaint.objects.get(topicid=self.tp, userid=self.us)
            from bbs.dao import BBSDao
            dao = BBSDao({'bbs':self.tp})
            dao.update_Tcomplaint(method)
            dao.update_Tsave()
        elif self.op:
            cm = Complaint.objects.get(opinionid=self.op, userid=self.us)
            from bbs.dao import OpinDao
            dao = OpinDao({'op':self.op})
            dao.update_Ocomplaint(method)
            dao.update_save()
        if key=='state':
            cm.state = 'CANCEL'
        cm.save()
            
            
