#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^add/$', 'complaint.views.add'),
    url(r'^cancel/$', 'complaint.views.cancel'),
)
