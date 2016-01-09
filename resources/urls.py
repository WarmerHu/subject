#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'resources.views.into_resources'),
    url(r'^list/$', 'resources.views.get_resources'),
    url(r'^delete/(.+)$', 'collection.views.delete_collection'),
    url(r'^Clist/$', 'collection.views.into_a_collection'),
    url(r'^Clist/(.+)$', 'collection.views.get_a_collection'),
    url(r'^answer/check/$', 'collection.views.check_answer'),
)
