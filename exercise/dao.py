#coding:utf-8
'''
Created on 2015-12-14
@author: 
description:读取数据库
'''
from subject.models import Exercise, User

'''
读取1条题目:迭代一——按顺序读取一条数据
'''
def read_a_title(req=1):
    e = Exercise.objects.filter()[int(req)-1 : req]
    rsp = {}
    for v in e:
        rsp['id'] = v.id
        rsp['title'] = v.title
        rsp['state'] = v.state
        rsp['author'] = v.userid.username
    return rsp

def get_tips_byId(req):
    e = Exercise.objects.get(id=req)
    return e.tips

def select_title_byReq(self,req):
    if req.has_key('id'):
        return Exercise.objects.get(id=req['id'])

    

class exerciseDao():
    def __init__(self,req):
        if req.has_key('username'):
            self.us = User.objects.get(username=req['username'])
        elif req.has_key('userid'):
            self.us = User.objects.get(id=req['userid'])
    
    def insert_a_title(self,req):
        Exercise(title=req['title'],answer=req['answer'],tips=req['tips'],userid=self.us,state='ACTIVE').save()
    
    def insert_titles(self,req):
        querysetlist=[]
        for i in req:
            querysetlist.append(Exercise(title=i['title'],
                                         answer=i['answer'],
                                         tips=i['tips'],
                                         userid=self.us,
                                         state='ACTIVE'))        
        Exercise.objects.bulk_create(querysetlist)
    

