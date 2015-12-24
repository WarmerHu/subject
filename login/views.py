#coding:utf-8
from django.shortcuts import render, render_to_response
from subject.models import User
from django.http.response import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.utils import simplejson
import json
from django.views.decorators.csrf import csrf_exempt

def login_page(req):
    return render_to_response('login.html',context_instance=RequestContext(req))

@csrf_exempt
def login(req):
    info = 'end'
    try:
        if req.method == 'POST':
            jsonReq = simplejson.loads(req.body)
            userna = jsonReq['username']
#            password = jsonReq['password']
            user = User.objects.filter(username = userna,password = jsonReq['password'])
            if user:
                response = HttpResponse()
                response.set_cookie('name', userna, 3600)
                return response
            else:
                return HttpResponse(json.dumps({'error':'error'}),content_type='application/json')
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    return HttpResponse(json.dumps({'error':info}),content_type="application/json")
    
    
def logout(req):
    pass

def regist(req):
    pass
