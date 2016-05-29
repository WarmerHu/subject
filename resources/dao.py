#coding:utf-8
'''
Created on 2016年1月10日

@author: warmerhu
'''
from subject.models import Source, User
from subject import settings
from subject.globalData import ONE_PAGE_NUM
from activity.dao import is_activity
def select_Cresource():
    return Source.objects.count()

def select_resources(page,us=None):
    q = '''select * 
            from source  
            order by content desc;'''
#     s = Source.objects.order_by("-content")[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
    s = Source.objects.raw(q)[(page-1)*ONE_PAGE_NUM:page*ONE_PAGE_NUM]
    rsp = []
    for v in s:
        content = {}
        content['id'] = v.id
        content['uploader'] = v.userid.id
        content['downloaded'] = v.content
        content['money'] = v.points
        content['downloader'] = v.download
        if us:
            from complaint.dao import complaintDao
            dao = complaintDao({"userid":us, "rsid":v.id})
            content['complaint'] = dao.is_complaint_byRS()
            q = (dao.us.username + ("  下载资源: ").decode("utf-8") + v.download).encode("utf-8")
#             w = "warmer 下载资源: test.py"
            content['dw'] =  is_activity(q)
#             content['dw'] =  q
        rsp.append(content)
    return rsp

class rsUpdateDao:
    def __init__(self,rss=0,rsid=0):
        if rss:
            self.rs = rss
        if rsid:
            self.rs = Source.objects.get(id = rsid)
    
    def update_content(self):
            self.rs.content += 1
            return self.rs.content

    def update_state(self, st="ACTIVE"):
        self.rs.state = st
    
    def update_complaint(self,method="+"):
        if method=="+":
            self.rs.complaint += 1
        elif method=="-":
            self.rs.complaint -= 1
        return self.rs.complaint
     
    def update_save(self):
        self.rs.save()    
        
class resourcesDao:
    def __init__(self,req):
        if req.has_key("username"):
            self.us = User.objects.get(username=req["username"])
        elif req.has_key("id"):
            self.us = User.objects.get(id=req["id"])
                
    def insert_a_resources(self,req):
        Source(userid=self.us,content=0,points=req['points'],download=req['path']).save()

def uploadFile(req):
    f_path = settings.MEDIA_ROOT + req['filename']
    with open(f_path,'w') as info:
        for chunk in req['file'].chunks():
            info.write(chunk)
    resourcesDao({"id":req['userid']}).insert_a_resources({'points':req['points'],'path':req['filename']})
