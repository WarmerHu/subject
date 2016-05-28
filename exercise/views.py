#coding=utf-8
from django.shortcuts import  render_to_response
from django.template.context import RequestContext

from collection.dao import collectionDao
from django.http.response import HttpResponse
import json
from activity.dao import activityDao
from django.utils import simplejson
from subject.models import Exercise
from django.views.decorators.csrf import csrf_exempt
from login.dao import userDao
from exercise.controller import fileCon
from exercise.dao import read_a_title, get_tips_byId, exerciseDao, updateEXDao


def into_title(req):
    if req.COOKIES.has_key('userid'):
        userid = req.COOKIES['userid'] 
        content = ('进入刷题宝典').decode('utf-8')
        ADao = activityDao({"userid":userid})
        ADao.add_a_activity(content)
        return render_to_response('title.html',RequestContext(req))
    return render_to_response('login.html',RequestContext(req))

#获取一条题目
def get_title(req,param):
    if req.COOKIES.has_key('userid'):
        rsp = read_a_title(req=param,userid=req.COOKIES['userid'] )
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
    if req.method=='POST' and req.COOKIES.has_key('userid'):
        jsonReq = simplejson.loads(req.body)
        titleId = jsonReq['id']
        titleAs = jsonReq['answer']
        usid = req.COOKIES['userid']
        if titleAs:
            isTitle = Exercise.objects.filter(id = titleId,answer = titleAs)
            if isTitle:
                dao = userDao({'userid':usid})
                dao.update_point_byReq({'method':'+','points':1})
                dao.save_update()
                rsp = read_a_title(req=jsonReq['num'],userid=usid)
                return HttpResponse(json.dumps(rsp), content_type="application/json")
        rsp = {'exerciseid':titleId,'userid':usid}
        CDao = collectionDao(rsp)
        if not CDao.select_collection_byExUs():
            CDao.insert_collection()    
        return HttpResponse(json.dumps({'tips':get_tips_byId(titleId)}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'请输入正确的答案'}), content_type="application/json")


def into_publish(req):
    if req.COOKIES.has_key('userid'):
        return render_to_response('publish.html',RequestContext(req))
    return render_to_response('login.html',RequestContext(req))

'''
发布题目:1.获取登录信息
        2.储存数组里的内容
'''
@csrf_exempt
def publish_title(req):
    if req.method=='POST' and req.COOKIES.has_key('userid'):
        method = str(req.GET.get('p'))
        userid = req.COOKIES['userid'] 
        if method == 'input':
            jsonReq = simplejson.loads(req.body)
            ED = exerciseDao({'userid':userid})
            for v in jsonReq:
                ED.insert_a_title(v)
            content = ('发布了题目').decode('utf-8')
            ADao = activityDao({"userid":userid})
            ADao.add_a_activity(content)
            return HttpResponse(json.dumps({'tips':'添加成功'}), content_type="application/json")
        elif method == 'upload':
            if not exerciseDao({'userid':userid}).if_excel():
                file = req.FILES['uploadedfile']  # @ReservedAssignment
                filename = req.POST['filename'].encode('utf-8')
                if file:
                    tips = fileCon({'filename':filename,'file':file,'userid':userid})
            else:
                tips = "今天已上传了excel"
            return HttpResponse(json.dumps({'tips':tips}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'添加失败'}), content_type="application/json")

'''
request body:{'titleid':xxx, 'authorid':xxx}
'''
@csrf_exempt
def contribute(req):
    if req.method=='POST' and req.COOKIES.has_key('userid'):
        jsonReq = simplejson.loads(req.body)
        dao = updateEXDao(ex=jsonReq['titleid'])
        dao.update_exercise_points()
        dao.update_ex_save()
        dao = userDao({'userid':jsonReq['authorid']})
        dao.update_point_byReq({'method':'+','points':1})
        dao.save_update()
        return HttpResponse(json.dumps({'tips':'点赞成功'}), content_type="application/json")
    return HttpResponse(json.dumps({'tips':'点赞失败'}), content_type="application/json")
            
            