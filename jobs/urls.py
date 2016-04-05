#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'jobs.views.into_jobs'),
    url(r'^list/$', 'jobs.views.get_jobs'),
)
