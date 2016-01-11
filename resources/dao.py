#coding:utf-8
'''
Created on 2016年1月10日

@author: warmerhu
'''
from subject.models import Source, User
from subject import settings
def select_resources():
    s = Source.objects.all()
    rsp = []
    content = {}
    for v in s:
        content['id'] = v.id
        content['uploader'] = v.userid.id
        content['downloaded'] = v.content
        content['money'] = v.points
        content['downloader'] = v.download
        rsp.append(content)
    return rsp

class resourcesDao():
    def __init__(self,req):
        if req.has_key("username"):
            self.us = User.objects.get(username=self.us)
                
    def insert_a_resources(self,req):
        Source(userid=self.us,content=0,points=0,download=req)

def uploadFile(req):
    f_path = settings.MEDIA_URL + req['file'].name
    with open(f_path,'wb+') as info:
        print req['file'].name
        for chunk in req.chunks():
            info.write(chunk)
    resourcesDao(req['username']).insert_a_resources(f_path)