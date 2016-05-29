#!/usr/bin/python
#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import simplejson
from complaint.dao import complaintDao
from django.http.response import HttpResponse
import json
from activity.dao import activityDao, is_activity
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from subject.models import User


def into_complaint(req):
    return render_to_response('complaint.html',RequestContext(req))

def get_complaintFromMe(req):
    if req.COOKIES.has_key("userid"):
        userid = req.COOKIES["userid"]
        p = int(req.GET.get('p'))
#         cur = p
#         rs = {}
#         if p==0:
#             cur = 1
#             cn = select_Ccomplaint()
#             rs['numT'] = cn
#         rs['result'] = complaintDao({'userid':userid}).select_complaint_byUS(cur)
        return HttpResponse(json.dumps(complaintDao({'userid':userid}).select_complaint_byUS(p)), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'未登录'}), content_type="application/json")
    
def get_myComplaint(req):
    if req.COOKIES.has_key("userid"):
        userid = req.COOKIES["userid"]
        p = int(req.GET.get('p'))
#         cur = p
#         rs = {}
#         if p==0:
#             cur = 1
#             cn = select_Ccomplaint()
#             rs['numT'] = cn
#         rs['result'] = complaintDao({'authorid':userid}).select_complaint_byAU(cur)
        return HttpResponse(json.dumps(complaintDao({'authorid':userid}).select_complaint_byAU(p)), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'未登录'}), content_type="application/json")

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
        actDao = activityDao({"userid":userid})
        if jsonReq.has_key('titleid'):
            titleid = jsonReq['titleid']
            dao = complaintDao({'userid':userid,'titleid':titleid})
            if dao.is_complaint_byEX():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
            activities = " complaints for the title published by "+dao.us.username
        elif jsonReq.has_key('authorid'):
            authorid = jsonReq['authorid']
            dao = complaintDao({'userid':userid,'authorid':authorid})
            if dao.is_complaint_byAU():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
            activities = " complaints for "+dao.au.username
        elif jsonReq.has_key('topicid'):
            topicid = jsonReq['topicid']
            dao = complaintDao({'userid':userid,'topicid':topicid})
            if dao.is_complaint_byTP():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
            activities = " complaints for "+dao.tp.name
        elif jsonReq.has_key('opinionid'):
            opinionid = jsonReq['opinionid']
            dao = complaintDao({'userid':userid,'opinionid':opinionid})
            if dao.is_complaint_byOP():
                return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
            opdao = dao.op
            activities = " complaints for an opinion published by "+opdao.userid.username+" on "+opdao.topicid.name
        elif jsonReq.has_key('rsid'):
            rsid = jsonReq['rsid']
            dao = complaintDao({'userid':userid,'rsid':rsid})
            q = (dao.us.username + ("  下载资源: ").decode("utf-8") + dao.rs.download).encode("utf-8")
            if not is_activity(q):
                return HttpResponse(json.dumps({'tips':'假如你没有下载这份资源，你怎么知道资源的内容违反礼仪？'}), content_type="application/json")
            else:
                if dao.is_complaint_byRS():
                    return HttpResponse(json.dumps({'tips':'你已经投诉过了'}), content_type="application/json")
                rsdao = dao.rs
#                 activities = " complaints for a resource " + rsdao.download + " uploaded by "+ rsdao.userid.username   
                activities = '对'  + rsdao.userid.username + '发布的资源：' + rsdao.download + '进行投诉'   
        rq['content'] = jsonReq['content']
        actDao.add_a_activity(activities)
        return HttpResponse(json.dumps({'tips':dao.insert_a_complaint(rq,'+')}), content_type="application/json")
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
            dao.update_a_complaint(key='state',method='-')
        elif jsonReq.has_key('authorid'):
            dao = complaintDao({'userid':userid, 'authorid': jsonReq['authorid']})
            dao.update_a_complaint('state','-')
        elif jsonReq.has_key('topicid'):
            dao = complaintDao({'userid':userid, 'topicid': jsonReq['topicid']})
            dao.update_a_complaint('state','-')
        elif jsonReq.has_key('rsid'):
            dao = complaintDao({'userid':userid, 'rsid': jsonReq['rsid']})
            dao.update_a_complaint('state','-')
        elif jsonReq.has_key('opinionid'):
            dao = complaintDao({'userid':userid, 'opinionid': jsonReq['opinionid']})
            dao.update_a_complaint('state','-')
        elif jsonReq.has_key('authorid'):
            dao = complaintDao({'userid':userid, 'authorid': jsonReq['authorid']})
            dao.update_a_complaint('state','-')
        return HttpResponse(json.dumps({}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'请求格式不正确'}), content_type="application/json")
