#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'resources.views.into_resources'),
    url(r'^list/$', 'resources.views.get_resources'),
    url(r'^upload/$', 'resources.views.upload_resources'),
)
