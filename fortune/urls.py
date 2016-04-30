#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'fortune.views.into_fortune'),
    url(r'^list/$', 'fortune.views.get_fortune'),
)
