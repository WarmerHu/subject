#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'collection.views.into_collection'),
    url(r'^list/$', 'collection.views.get_collection'),
    url(r'^delete/(.+)$', 'collection.views.delete_collection'),
    url(r'^Clist/$', 'collection.views.into_a_collection'),
    url(r'^Clist/(.+)$', 'collection.views.get_a_collection'),
    url(r'^answer/check/$', 'collection.views.check_answer'),
    url(r'^note/$', 'collection.views.note'),
)
