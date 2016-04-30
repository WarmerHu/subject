#!/usr/bin/python
#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import simplejson
from complaint.dao import complaintDao
from django.http.response import HttpResponse
import json

'''
add a complaint:
request body:{'titleid'|'authorid' | 'topicid' | 'opinionid' :xx, 'content':xxx}
'''
@csrf_exempt
def add(req):
    if req.method=='POST' and req.COOKIES.has_key('userid'):
        jsonReq = simplejson.loads(req.body)
        rq = {}
        userid = req.COOKIES['userid']
        if jsonReq.has_key('titleid'):
            titleid = jsonReq['titleid']
            dao = complaintDao({'userid':userid,'titleid':titleid})
            if dao.is_complaint_byEX():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
        elif jsonReq.has_key('authorid'):
            authorid = jsonReq['authorid']
            dao = complaintDao({'userid':userid,'authorid':authorid})
            if dao.is_complaint_byAU():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
        elif jsonReq.has_key('topicid'):
            topicid = jsonReq['topicid']
            dao = complaintDao({'userid':userid,'topicid':topicid})
            if dao.is_complaint_byTP():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
        elif jsonReq.has_key('opinionid'):
            opinionid = jsonReq['opinionid']
            dao = complaintDao({'userid':userid,'opinionid':opinionid})
            if dao.is_complaint_byOP():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
        rq['content'] = jsonReq['content']
        return HttpResponse(json.dumps({'tips':dao.insert_a_complaint(rq)}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'请求格式不正确or未登录'}), content_type="application/json")

'''
add a complaint:
request body:{'titleid'|'authorid'| 'topicid' | 'opinionid' :xx}
'''
@csrf_exempt
def cancel(req):
    if req.method=='POST' and req.COOKIES.has_key('userid'):
        jsonReq = simplejson.loads(req.body)
        userid = req.COOKIES['userid']
        if jsonReq.has_key('titleid'):
            dao = complaintDao({'userid':userid,'titleid': jsonReq['titleid']})
            dao.update_a_complaint(key='state', obj='titleid',method='-')
        elif jsonReq.has_key('authorid'):
            dao = complaintDao({'userid':userid, 'authorid': jsonReq['authorid']})
            dao.update_a_complaint('state', 'authorid','-')
        elif jsonReq.has_key('topicid'):
            dao = complaintDao({'userid':userid, 'topicid': jsonReq['topicid']})
            dao.update_a_complaint('state', 'topicid','-')
        elif jsonReq.has_key('opinionid'):
            dao = complaintDao({'userid':userid, 'opinionid': jsonReq['opinionid']})
            dao.update_a_complaint('state', 'opinionid','-')
        return HttpResponse(json.dumps({'tips':'取消投诉成功'}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'请求格式不正确'}), content_type="application/json")
