#coding:utf-8
'''
Created on 2016年1月10日

@author: warmerhu
'''
from subject.models import Source
def select_resources():
    s = Source.objects.all()
    rsp = []
    content = {}
    for v in s:
        content['id'] = v.id
        content['uploader'] = v.userid.id
        content['downloaded'] = v.content
        content['money'] = v.points
        content['downloader'] = v.download
        rsp.append(content)
    return rsp
