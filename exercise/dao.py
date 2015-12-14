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
    e = Exercise.objects.all()[req:req]
    rsp = {}
    rsp['id'] = e.id
    rsp['title'] = e.title
    rsp['answer'] = e.answer
    return rsp
