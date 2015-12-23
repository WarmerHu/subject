#coding:utf-8
'''
Created on 2015-12-14
@author: 
description:读取数据库
'''
from subject.models import Exercise

'''
读取1条题目:迭代一——按顺序读取一条数据
'''
def read_a_title(req=1):
    e = Exercise.objects.all()[int(req)-1 : req]
    rsp = {}
    for v in e:
        rsp['id'] = v.id
        rsp['title'] = v.title
#        rsp['answer'] = (v.answer).encode('utf8')
#        rsp['tips'] = v.tips
    return rsp

def get_answer_byId(req):
    e = Exercise.objects.get(id=req)
    return e[0]['answer'],e[0]['tips']