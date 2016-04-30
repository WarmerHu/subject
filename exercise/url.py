#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'exercise.views.into_title'),
    url(r'^elist/(.+)/$', 'exercise.views.get_title'),
    url(r'^contribute/$', 'exercise.views.contribute'),
    url(r'^answer/check/$', 'exercise.views.check_answer'),
    url(r'^publish/add/$', 'exercise.views.into_publish'),
    url(r'^publish/$', 'exercise.views.publish_title'),
)
