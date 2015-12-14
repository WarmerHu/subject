#coding=utf-8
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from exercise.dao import read_a_title
from django.http.response import HttpResponse
import json

# Create your views here.
'''
功能：1.主界面：
                        显示模块
                        点击后跳转
    2.显示题目：题目&答题区域
    3.校准答案
'''
def index(req):
    return render_to_response('test.html',RequestContext(req))


def get_title(req,param):
    rsp = read_a_title(param)
    return HttpResponse(json.dumps(rsp), content_type="application/json")