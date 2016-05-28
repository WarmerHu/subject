#coding:utf-8
'''
Created on 2016-1-5
@author: 
description:
'''
from subject.models import Collection, Exercise, User
from subject.globalData import ONE_PAGE_NUM
from django.db.models.query_utils import Q
from _dbus_bindings import String

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
        col = Collection.objects.filter(userid=self.us).order_by('-wrongtime')[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
        for v in col:
            if v.exerciseid.state=='NORMAL':
                title = {'id':v.exerciseid.id,'title':v.exerciseid.title,'answer':v.exerciseid.answer}
                val = {'id':v.id,'rightTime':v.righttime,'wrongTime':v.wrongtime,'note':v.note,'title':title}
                rsp.append(val)
        return rsp
    
    def select_a_collection_byUs(self,req=1):
        q  = '''select collection.id as id,exercise.id as exid,title,rightTime as rt,wrongTime as wt from collection,exercise 
                where collection.userId='''+String(self.us.id)+''' and exercise.state="NORMAL" and exerciseid=exercise.id limit '''+String(req)+''',1;'''
        e = Collection.objects.raw(q)
        rsp = {}
        title = {}
        for v in e:
            title['id'] = v.exid
            title['title'] = v.title
            rsp['id'] = v.id
            rsp['rightTime'] = v.rt
            rsp['wrongTime'] = v.wt
            rsp['title'] = title
        return rsp
    

