#coding:utf-8
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.utils import simplejson
import json
from django.views.decorators.csrf import csrf_exempt
from subject.models import User
from login.controller import time_control, mail_control
from login.dao import userDao

def index(req):
    return render_to_response('index.html',RequestContext(req))

def login_page(req):
    return render_to_response('login.html',context_instance=RequestContext(req))

@csrf_exempt
def login(req):
    if req.method == 'POST':
        jsonReq = simplejson.loads(req.body)
        userna = jsonReq['username']
        user = User.objects.filter(username = userna,password = jsonReq['password'])
        if user:
            if user[0].state=='NORMAL':
                return HttpResponse(json.dumps({'username':user[0].username,'id':user[0].id}),content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error':'该账号未激活！'}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'请输入正确的账号密码'}),content_type="application/json")
    
    
def logout(req):
    response = HttpResponseRedirect("/")
    response.delete_cookie("username", "/")
    return response

def regist_page(req):
    return render_to_response('regist.html',context_instance=RequestContext(req))

'''
注册：1.验证用户名、密码
2.发送激活邮件：邮件格式  xxx/account/active?un=加密名字&t=失效时间
        加密名字= 注册名，失效时间     2个参数一起加密的字符串 
    2.1激活邮件的验证：失效时间与当前时间比较，已失效，重新生成加密名字、发送激活邮件；未失效，成功激活用户
'''
@csrf_exempt
def regist(req):
    if req.method == 'POST':
        jsonReq = simplejson.loads(req.body)
        userna = jsonReq['username'].encode('utf-8')
        usere = jsonReq['email']
        if not User.objects.filter(username=userna) and not User.objects.filter(email=usere):
            unameDeadline = mail_control({'method':'regist','username':userna,'email':usere})
            User(username=userna,password=jsonReq['password'],email=usere,state='ACTIVE',points=0,flag=unameDeadline,head='test.jpg').save()
#             userDao({'username':userna.decode('utf-8')}).update_flag(unameDeadline)
            return HttpResponse(json.dumps({}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'请输入正确的未注册的用户名、邮箱'}),content_type="application/json")

def active(req):
    deadline = int(req.GET.get('t'))
    flag = req.GET.get('un').encode('utf-8')
    name = req.GET.get('name').encode('utf-8')
    now = int(time_control({'active':'active'}))
    if now <= deadline:
        dao = userDao({'username':name})
        if dao.us and dao.us.state=='ACTIVE':
#             if check_password(name+str(deadline), dao.us.flag):
            if flag == dao.us.flag.encode('utf-8'):
                dao.update_state('NORMAL')
                dao.save_update()
                return render_to_response('login.html',{'tips':'激活成功!'},context_instance=RequestContext(req))
            else:
                unameDeadline = mail_control({'method':'regist','username':name,'email':dao.us.email})
                dao.update_flag(unameDeadline)
                dao.save_update()
    return render_to_response('active.html',{'tips':'链接失效，已重新发送激活邮件！！'},context_instance=RequestContext(req))
    
  
def into_reset(req):
    return render_to_response('reset.html',context_instance=RequestContext(req))

@csrf_exempt
def reset(req):
    if req.method == 'POST':
        jsonReq = simplejson.loads(req.body)
        usere = jsonReq['email']
        if User.objects.filter(email=usere):
            dao = userDao({'email':usere})
            us = dao.us
            if us.state == 'NORMAL':
                unameDeadline = mail_control({'method':'regist','username':us.username.encode('utf-8'),'email':usere})
                dao.update_flag(unameDeadline)
                dao.update_ps(jsonReq['password'])
                dao.update_state('ACTIVE')
                dao.save_update()
                return HttpResponse(json.dumps({}),content_type='application/json')
    return HttpResponse(json.dumps({'error':'请输入正确的已激活邮箱'}),content_type="application/json")

def into_account(req):
    if req.COOKIES.has_key('userid'):
        return render_to_response('account.html',context_instance=RequestContext(req))
    return render_to_response('login.html',context_instance=RequestContext(req))
    
