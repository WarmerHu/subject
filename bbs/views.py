#coding=utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
from bbs.dao import select_Ctopic, select_topics_byReq, BBSDao
import re
from login.dao import userDao
from _dbus_bindings import String

def into_bbs(req):
    return render_to_response('bbs.html',RequestContext(req))

@csrf_exempt
def get_bbs(req):
    p = int(req.GET.get('p'))
    cur = p
    rs = {}
    if p==0:
        cur = 1
        cn = select_Ctopic()
        rs['numT'] = cn
    ts = select_topics_byReq({"method":"-","column":"modifytime"},cur)
    rs['topic'] = ts
    return HttpResponse(json.dumps(rs),content_type="application/json")
    
'''
发布话题：
1.验证提交方式 &验证登录信息:正确，下一步；否，返回{“tips”:"xxx"}
2.验证数据格式:正确，下一步；否，返回{“tips”:"xxx"}
3.插入数据库,获取返回信息：True，返回{}；False，返回{“tips”:"xxx"}
'''
@csrf_exempt
def add_a_bbs(req):
    if req.method == "POST" and req.COOKIES.has_key('username'):
        name = req.POST["name"]
        detail = req.POST["detail"]
        nlen = len(name)
        dlen = len(detail)
        if nlen<6 or nlen>50 or dlen<10 or dlen>10000:
            return HttpResponse(json.dumps({"tips":"请正确输入标题与详情，标题长度∈[6,50]，详情长度∈[10,10000]"}),content_type="application/json")
        else:
            dao = BBSDao({"userid":req.COOKIES["userid"]}) 
            if dao.insert_a_topic({"name":name,"content":detail}):
                return HttpResponse(json.dumps(dao.select_newestTopic_byUs()),content_type="application/json")
    return HttpResponse(json.dumps({"tips":"登录用户一天内最多可发布5则话题"}),content_type="application/json")

def into_a_bbs(req):
    return render_to_response('a_bbs.html',RequestContext(req))


def get_topic(req,param):
    dao = BBSDao({"id":int(param)})
    if req.COOKIES.has_key('userid'):
        dao = dao.select_topic(us=req.COOKIES['userid'])
    else:
        dao = dao.select_topic()
    return HttpResponse(json.dumps(dao),content_type="application/json")

def get_opinions(req,param):
    p = int(req.GET.get('p'))
    cur = p
    rs = {}
    dao = BBSDao({"id":int(param)})
    if p==0:
        cur = 1
        cn = dao.select_Copinion_byBBS()
        rs['numT'] = cn
    if req.COOKIES.has_key('userid'):
        rs['opinion'] = dao.select_opinions_byBBS(cur,us=req.COOKIES['userid'])
    else:
        rs['opinion'] = dao.select_opinions_byBBS(cur)
    return HttpResponse(json.dumps(rs),content_type="application/json")
 
@csrf_exempt
def add_a_opinion(req,param):
    if req.method == "POST" and req.COOKIES.has_key('userid'):
        content = req.POST["content"]
        auTp = int(req.POST["auTp"]) #发布话题的作者
        au = int(req.POST["au"]) #用户quote
        op = req.POST["op"]
        ph = req.POST["ph"]
        userid = req.COOKIES["userid"]
        dlen = len(content)
        if dlen<10 or dlen>10000:
            return HttpResponse(json.dumps({"tips":"请正确输入意见，长度∈[10,10000]"}),content_type="application/json")
        else:
            dao = BBSDao({"userid":userid,"id":int(param),'au':auTp}) 
            if dao.insert_a_opinion({"content":content,"userid":userid}):
                if au and op and ph:
                    regLIST = "<b>"+('引用').decode("utf-8")+"<a href='"+op+"'>"+ph+"</a>"+("的意见").decode("utf-8")+"</b>"
                    if re.match(regLIST,content):
                        dao = userDao({'userid':int(au)})
                        dao.update_point_byReq({'method':"+",'points':1})
                        dao.save_update()
                return HttpResponse(json.dumps({}),content_type="application/json")
    return HttpResponse(json.dumps({"tips":"登录用户每min只可发布一条意见"}),content_type="application/json")

        