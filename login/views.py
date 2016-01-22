#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.utils import simplejson
import json
from django.views.decorators.csrf import csrf_exempt
from subject.models import User

def login_page(req):
    return render_to_response('login.html',context_instance=RequestContext(req))

@csrf_exempt
def login(req):
    info = 'end'
    try:
        if req.method == 'POST':
            jsonReq = simplejson.loads(req.body)
            userna = jsonReq['username']
            user = User.objects.filter(username = userna,password = jsonReq['password'])
            if user:
                return HttpResponse(json.dumps({'username':user[0].username,'id':user[0].id}),content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error':'请输入正确的账号密码'}),content_type='application/json')
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    return HttpResponse(json.dumps({'error':info}),content_type="application/json")
    
    
def logout(req):
    response = HttpResponseRedirect("/")
    response.delete_cookie("username", "/")
    return response

def regist_page(req):
    return render_to_response('regist.html',context_instance=RequestContext(req))

@csrf_exempt
def regist(req):
    info = 'end'
    try:
        if req.method == 'POST':
            jsonReq = simplejson.loads(req.body)
            userna = jsonReq['username']
            usere = jsonReq['email']
            if User.objects.filter(username=userna) or User.objects.filter(email=usere):
                return HttpResponse(json.dumps({'error':'用户名 or 邮箱已注册'}),content_type='application/json')
            else: 
                User(username=userna,password=jsonReq['password'],email=usere,state='ACTIVE',points=0).save()
                return HttpResponse(json.dumps({'username':userna,}),content_type='application/json')
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    return HttpResponse(json.dumps({'error':info}),content_type="application/json")
