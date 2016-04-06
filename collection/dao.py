#coding:utf-8
'''
Created on 2016-1-5
@author: 
description:
'''
from subject.models import Collection, Exercise, User
from subject.globalData import ONE_PAGE_NUM

def update_rightTime_byReq(req):
    if req.has_key('id'):
        dao = Collection.objects.get(id=req['id'])
        dao.righttime += 1
        dao.save()
    
def update_wrongTime_byReq(req):
    if req.has_key('id'):
        dao = Collection.objects.get(id=req['id'])
        dao.wrongtime += 1
        dao.save()
    
def select_collection_byReq(req):
    if req.has_key('id'):
        return Collection.objects.get(id=req['id'])

class collectionDao():
    def __init__(self,req):
        if req.has_key('exerciseid'):
            self.ex = Exercise.objects.get(id=req['exerciseid'])
        self.us = User.objects.get(id = req['userid'])

    def insert_collection(self):
        Collection(exerciseid=self.ex,userid=self.us,wrongtime=1,righttime=0).save()
        return

    def select_collection_byExUs(self):
        col = Collection.objects.filter(userid=self.us,exerciseid=self.ex)
        if col:
            return True
        return False
    
    def select_Ccollection_byUs(self):
        return Collection.objects.filter(userid=self.us).count()
        
    def select_collection_byUs(self,page):
        rsp = []
        col = Collection.objects.filter(userid=self.us)[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
        for v in col:
            title = {'id':v.exerciseid.id,'title':v.exerciseid.title,'answer':v.exerciseid.answer}
            val = {'id':v.id,'rightTime':v.righttime,'wrongTime':v.wrongtime,'note':v.note,'title':title}
            rsp.append(val)
        return rsp
    
    def select_a_collection_byUs(self,req=1):
        e = Collection.objects.filter(userid=self.us)[int(req)-1 : req]
        rsp = {}
        title = {}
        for v in e:
            title['id'] = v.exerciseid.id
            title['title'] = v.exerciseid.title
            rsp['id'] = v.id
            rsp['rightTime'] = v.righttime
            rsp['wrongTime'] = v.wrongtime
            rsp['note'] = v.note
            rsp['title'] = title
            return rsp
    

