#coding:utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse, StreamingHttpResponse
import json
from resources.dao import select_resources, uploadFile,\
    select_Cresource, rsUpdateDao
from django.views.decorators.csrf import csrf_exempt
from subject.models import User, Source
from activity.dao import activityDao
from login.dao import userDao
from subject import settings

def into_resources(req):
    return render_to_response('resources.html',RequestContext(req))

def get_resources(req):
    p = int(req.GET.get('p'))
    cur = p
    rs = {}
    if p==0:
        cur = 1
        cn = select_Cresource()
        rs['numT'] = cn
    us = None
    if req.COOKIES.has_key("userid"):
        us = req.COOKIES["userid"]
    rs['res'] = select_resources(cur,us)
    return HttpResponse(json.dumps(rs),content_type="application/json")

 
@csrf_exempt
def upload_resources(req):
    if req.COOKIES.has_key('userid'):
        file = req.FILES['uploadedfile']  # @ReservedAssignment
        points = req.POST['points']
        filename = req.POST['filename'].encode('utf-8')
        if file:
            userid = req.COOKIES['userid'].decode('utf-8').encode('utf-8')
            uploadFile({'userid':userid,'file':file,'filename':filename,'points':points})
            content = ' 上传资源：' + filename 
            ADao = activityDao({"userid":userid})
            ADao.add_a_activity(content.decode('utf-8'))
            return HttpResponse(json.dumps({'tips':'上传成功'}),content_type="application/json")  
    return HttpResponse(json.dumps({'tips':'上传失败or未登录'}),content_type="application/json") 

'''
下载时的积分处理：
1.获取登录信息：成功，下一步；失败，返回错误信息
2.获取传递参数
3.判断下载者积分：充足，下一步；否，返回错误信息
4.减少下载者积分，增加上传者积分
5.返回空白json
'''
# @csrf_exempt
def download_resources(req):
    if req.COOKIES.has_key('userid'):
        resourceID = int(req.GET.get('rs'))
        downloader = req.COOKIES['userid']
        dao = Source.objects.get(id=resourceID)
        downloadPoint = dao.points
        uploader = dao.userid
#         downloadPoint = int(req.POST["points"])
#         uploader = int(req.POST["uploader"])
#         resourceID = int(req.POST["resourceID"])
        if User.objects.filter(id=downloader,points__gte=downloadPoint):
            dao = userDao({'userid':downloader})
            dao.update_point_byReq({'method':'-','points':downloadPoint})
            dao.save_update() 
            dao = userDao({'us':uploader})
            dao.update_point_byReq({'method':'+','points':downloadPoint})
            dao.save_update()
            dao = rsUpdateDao(rsid=resourceID)
            count = dao.update_content()
            dao.update_save()
            content = (' 下载资源: ').decode("utf-8") + dao.rs.download
            downloadPath = settings.MEDIA_ROOT+dao.rs.download  
            ADao = activityDao({"userid":downloader})
            ADao.add_a_activity(content)
            
            def file_iterator(file_name, chunk_size=512):
                with open(file_name) as f:
                    while True:
                        c = f.read(chunk_size)
                        if c:
                            yield c
                        else:
                            break
            
            response = StreamingHttpResponse(file_iterator(downloadPath))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(dao.rs.download) #默认文件名
            return response
#             return HttpResponse(json.dumps({'resourceID':resourceID,"count":count,'dURL':downloadURL}),content_type="application/json")
        return  HttpResponse('积分不足')
    return  HttpResponse('请先登录')