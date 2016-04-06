#coding:utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse
import json
from resources.dao import select_resources, uploadFile, update_a_resources_byReq,\
    select_Cresource
from django.views.decorators.csrf import csrf_exempt
from subject.models import User
from activity.dao import activityDao
from login.dao import userDao

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
    rs['res'] = select_resources(cur)
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
            content = '上传资源：' + filename 
            ADao = activityDao({"userid":userid})
            ADao.add_a_activity(content)
            return HttpResponse(json.dumps({'tips':'上传成功'}),content_type="application/json")  
    return HttpResponse(json.dumps({'tips':'上传失败'}),content_type="application/json") 

'''
下载时的积分处理：
1.获取登录信息：成功，下一步；失败，返回错误信息
2.获取传递参数
3.判断下载者积分：充足，下一步；否，返回错误信息
4.减少下载者积分，增加上传者积分
5.返回空白json
'''
@csrf_exempt
def download_resources(req):
    if req.COOKIES.has_key('userid'):
        downloader = req.COOKIES['userid']
        downloadPoint = int(req.POST["points"])
        uploader = int(req.POST["uploader"])
        resourceID = int(req.POST["resourceID"])
        if User.objects.filter(id=downloader,points__gte=downloadPoint):
            userDao({'userid':downloader}).update_point_byReq({'method':'-','points':downloadPoint}) 
            userDao({'userid':uploader}).update_point_byReq({'method':'+','points':downloadPoint})
            count = update_a_resources_byReq({'id': resourceID})
            content = '下载资源' 
            ADao = activityDao({"userid":downloader})
            ADao.add_a_activity(content)
            return HttpResponse(json.dumps({'resourceID':resourceID,"count":count}),content_type="application/json")
        return  HttpResponse(json.dumps({'tips':'积分不足'}),content_type="application/json")
    return  HttpResponse(json.dumps({'tips':'请先登录'}),content_type="application/json")