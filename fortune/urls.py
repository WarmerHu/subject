#coding:utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^list/$', 'fortune.views.get_fortune'),
)
