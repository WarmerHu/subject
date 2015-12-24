#coding:utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^go_login/$', 'login.views.login_page'),
                       url(r'^login/$', 'login.views.login'),

                       url(r'^regist/$', 'login.views.regist'),
                       url(r'^logout/$', 'login.views.logout'),
)
