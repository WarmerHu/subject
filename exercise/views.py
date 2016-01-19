#coding=utf-8
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from collection.dao import collectionDao
from exercise.dao import read_a_title, get_tips_byId, exerciseDao
from django.http.response import HttpResponse
import json
from activity.dao import activityDao
from django.utils import simplejson
from subject.models import Exercise, Collection, User
from django.views.decorators.csrf import csrf_exempt
from login.dao import get_id_byName, update_point_byReq


def index(req):
    return render_to_response('index.html',RequestContext(req))

def into_title(req):
    if req.COOKIES.has_key('username'):
        username = req.COOKIES['username'] 
        content = username +'进入刷题宝典'
        ADao = activityDao({"username":username})
        ADao.add_a_activity(content)
        return render_to_response('title.html',RequestContext(req))
    return render_to_response('login.html',RequestContext(req))

#获取一条题目
def get_title(req,param):
    if req.COOKIES.has_key('username'):
        rsp = read_a_title(param)
        return HttpResponse(json.dumps(rsp), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'获取失败，请重新登录'}), content_type="application/json")


'''
检查答案：1.获取登录信息
            2.核对答案：正确：获取积分，更新下一题
                        错误：插入错题集：检查错题是否存在：存在
                                                        不存在：插入
                                        返回tips
'''
@csrf_exempt
def check_answer(req):
    if req.method=='POST' and req.COOKIES.has_key('username'):
        jsonReq = simplejson.loads(req.body)
        titleId = jsonReq['id']
        titleAs = jsonReq['answer']
        reqNa = req.COOKIES['username']
        if titleAs:
            isTitle = Exercise.objects.filter(id = titleId,answer = titleAs)
            if isTitle:
                update_point_byReq({'username':reqNa,'method':'+','points':1})
                rsp = read_a_title(jsonReq['num'])
                return HttpResponse(json.dumps(rsp), content_type="application/json")
        rsp = {'exerciseid':titleId,'username':reqNa}
        print ("rsp:",rsp)
        CDao = collectionDao(rsp)
        if not CDao.select_collection_byExUs():
            CDao.insert_collection()    
        return HttpResponse(json.dumps({'tips':get_tips_byId(titleId)}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'请输入正确的答案'}), content_type="application/json")


def into_publish(req):
    if req.COOKIES.has_key('username'):
        userNa = get_id_byName(req.COOKIES['username'])
        content = req.COOKIES['username']+'发布了题目'
        ADao = activityDao(userNa)
        ADao.add_a_activity(content)
        return render_to_response('publish.html',RequestContext(req))
    return render_to_response('login.html',RequestContext(req))

'''
发布题目:1.获取登录信息
        2.储存数组里的内容
'''
@csrf_exempt
def publish_title(req):
    if req.method=='POST' and req.COOKIES.has_key('username'):
        jsonReq = simplejson.loads(req.body)
        ED = exerciseDao({'username':req.COOKIES['username']})
        for v in jsonReq:
            ED.insert_a_title(v)
        return HttpResponse(json.dumps({'tips':'添加成功'}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'添加失败'}), content_type="application/json")
            
            