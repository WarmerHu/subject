#coding=utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
from bbs.dao import BBSDao, select_topics_byReq

def into_bbs(req):
    return render_to_response('bbs.html',RequestContext(req))

@csrf_exempt
def get_bbs(req):
    return HttpResponse(json.dumps(select_topics_byReq({"method":"-","column":"modifytime"})),content_type="application/json")
    
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
        if nlen<6 or nlen>20 or dlen<10 or dlen>10000:
            return HttpResponse(json.dumps({"tips":"请正确输入标题与详情，标题长度∈[6,20]，详情长度∈[10,10000]"}),content_type="application/json")
        else:
            dao = BBSDao({"userid":req.COOKIES["userid"]}) 
            if dao.insert_a_topic({"name":name,"content":detail}):
                return HttpResponse(json.dumps(dao.select_newestTopic_byUs()),content_type="application/json")
    return HttpResponse(json.dumps({"tips":"登录用户一天内最多可发布5则话题"}),content_type="application/json")

def into_a_bbs(req):
    return render_to_response('a_bbs.html',RequestContext(req))


def get_topic(req,param):
    return HttpResponse(json.dumps(BBSDao({"id":int(param)}).select_topicOpinions()),content_type="application/json")
 
@csrf_exempt
def add_a_opinion(req,param):
    if req.method == "POST" and req.COOKIES.has_key('userid'):
        content = req.POST["content"]
        userid = req.COOKIES["userid"]
        dlen = len(content)
        if dlen<10 or dlen>10000:
            return HttpResponse(json.dumps({"tips":"请正确输入意见，长度∈[10,10000]"}),content_type="application/json")
        else:
            dao = BBSDao({"userid":userid,"id":int(param)}) 
            if dao.insert_a_opinion({"content":content,"userid":userid}):
                return HttpResponse(json.dumps({}),content_type="application/json")
    return HttpResponse(json.dumps({"tips":"登录用户每min只可发布一条意见"}),content_type="application/json")

        