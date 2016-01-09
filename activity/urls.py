#coding:utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'exercise.views.into_title'),
    url(r'^elist/(.+)/$', 'exercise.views.get_title'),
    url(r'^answer/check/$', 'exercise.views.check_answer'),
)
