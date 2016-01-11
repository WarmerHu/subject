#coding:utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse
import json
from resources.dao import select_resources, uploadFile
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def into_resources(req):
    return render_to_response('resources.html',RequestContext(req))

def get_resources(req):
    return HttpResponse(json.dumps(select_resources()),content_type="application/json")

 
 

@csrf_exempt
@csrf_protect
def upload_resources(req):
    if req.COOKIES.has_key('username'):
        file = req.FILES.get('uploadedfile',None)
        if file:              
            if uploadFile({'username':req.COOKIES['username'],'file':file}):
                return HttpResponse(json.dumps({'tips':'上传成功'}),content_tyoe="application/json")  
    return HttpResponse(json.dumps({'tips':'上传失败'}),content_tyoe="application/json")  