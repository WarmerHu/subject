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
    e = Exercise.objects.all()[req-1:req]
    print e
    rsp = {}
    for v in e:
        rsp['id'] = v.id
        rsp['title'] = v.title
        rsp['answer'] = (v.answer).encode('utf8')
    return rsp
