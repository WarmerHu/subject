#coding:utf-8
from django.shortcuts import render, render_to_response, get_object_or_404
from login.dao import get_id_byName
from activity.dao import activityDao
from django.template.context import RequestContext
from collection.dao import collectionDao, select_collection_byReq,\
    update_rightTime_byReq, update_wrongTime_byReq
from django.http.response import HttpResponse
import json
from subject.models import Collection, Exercise
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from exercise.dao import get_tips_byId

def into_collection(req):
    if req.COOKIES.has_key('username'):
        userNa = get_id_byName(req.COOKIES['username'])
        content = req.COOKIES['username']+'进入错题集'
        ADao = activityDao(userNa)
        ADao.add_a_activity(content)
        return render_to_response('collection.html',RequestContext(req))
    return render_to_response('login.html',RequestContext(req))

def get_collection(req):
    if req.COOKIES.has_key('username'):
        dataVal = collectionDao({'username':req.COOKIES['username']}).select_collection_byUs()
        return HttpResponse(json.dumps(dataVal),content_type="application/json")
    return HttpResponse(json.dumps({}),content_type="application/json")

@csrf_exempt
def delete_collection(req,p1):
    if select_collection_byReq({'id':p1}).righttime > 0:
        col = get_object_or_404(Collection,id=p1)
        col.delete()
        return HttpResponse()
    return HttpResponse(json.dumps({'tips':'唯有正确次数>0才能删除'}),content_type="application/json")
        

def into_a_collection(req):
    if req.COOKIES.has_key('username'):
        return render_to_response('a_collection.html',RequestContext(req))
    return render_to_response('login.html',RequestContext(req))   

#获取一条错题
def get_a_collection(req,param):
    if req.COOKIES.has_key('username'):
        rsp = collectionDao({'username':req.COOKIES['username']}).select_a_collection_byUs(param)
        return HttpResponse(json.dumps(rsp), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")

'''
验证错题答案：1.获取登录信息
        2.获取json
        3.判断答案：根据题目id、answer get——》存在：根据collection.id增加正确次数，返回下一错题详情
                                        不存在：根据collection.id增加错误次数，返回tips
'''
@csrf_exempt
def check_answer(req):
    if req.method=='POST' and req.COOKIES.has_key('username'):
        jsonReq = simplejson.loads(req.body)
        title = jsonReq['title']
        id = jsonReq['id']
        isTitle = Exercise.objects.filter(id = title['id'],answer = title['answer'])
        CDao = collectionDao({'username':req.COOKIES['username']})
        if isTitle:
            update_rightTime_byReq({'id':id})
            rsp = CDao.select_a_collection_byUs(jsonReq['num'])
            return HttpResponse(json.dumps(rsp), content_type="application/json")
        else:
            update_wrongTime_byReq({'id':id})
            return HttpResponse(json.dumps({'tips':get_tips_byId(title['id']),'wrongTime':select_collection_byReq({'id':id}).wrongtime}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'访问错误,请重新登录'}), content_type="application/json")
