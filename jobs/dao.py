#coding:utf-8
'''
Created on 2016年1月21日

@author: Warmer
'''
from subject.models import Jobs
from django.utils import timezone

def select_jobs():
    dao = Jobs.objects.order_by("-createtime")
    rsp = []
    for v in dao:
        value = {}
        value["id"] = v.id
        value["position"] = v.position
        value["company"] = v.company
        value["createtime"] = timezone.localtime(v.createtime).strftime('%Y-%m-%d')
        value["duty"] = v.duty
        value["contact"] = v.contact
        value["source"] = v.source
        rsp.append(value)
    return rsp

def insert_jobs(req):
    querysetlist=[]
    for i in req:
        querysetlist.append(Jobs(position=i["position"],
                                 company=i["company"],
                                 createtime=i["createtime"],
                                 duty=i["duty"],
                                 contact=i["contact"],
                                 source=i["source"]))        
    Jobs.objects.bulk_create(querysetlist)