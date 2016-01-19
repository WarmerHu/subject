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
    for v in s:
        content = {}
        content['id'] = v.id
        content['uploader'] = v.userid.id
        content['downloaded'] = v.content
        content['money'] = v.points
        content['downloader'] = v.download
        rsp.append(content)
    return rsp

def update_a_resources_byReq(req):
    if req.has_key('id'):
        s = Source.objects.get(id = req['id'])
    s.content += 1
    s.save()
    return s.content

class resourcesDao():
    def __init__(self,req):
        if req.has_key("username"):
            self.us = User.objects.get(username=req["username"])
        elif req.has_key("id"):
            self.us = User.objects.get(id=req["id"])
                
    def insert_a_resources(self,req):
        Source(userid=self.us,content=0,points=req['points'],download=req['path']).save()
    
    


def uploadFile(req):
    f_path = settings.MEDIA_ROOT + req['filename']
    print f_path
    with open(f_path,'wb+') as info:
        for chunk in req['file'].chunks():
            info.write(chunk)
    resourcesDao({"username":req['username']}).insert_a_resources({'points':req['points'],'path':req['filename']})
