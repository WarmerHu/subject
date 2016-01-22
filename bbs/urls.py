#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'bbs.views.into_bbs'),
    url(r'^list/$', 'bbs.views.get_bbs'),
    url(r'^publish/$', 'bbs.views.add_a_bbs'),
    url(r'^topic/$', 'bbs.views.into_a_bbs'),
    url(r'^topic/list/(.+)$', 'bbs.views.get_topic'),
    url(r'^topic/(.+)/publish$', 'bbs.views.add_a_opinion'),
)
