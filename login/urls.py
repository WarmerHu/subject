#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^go_login/$', 'login.views.login_page'),
                       url(r'^login/$', 'login.views.login'),

                       url(r'^go_regist/$', 'login.views.regist_page'),
                       url(r'^regist/$', 'login.views.regist'),
                       url(r'^active/$', 'login.views.active'),
                       
                       url(r'^go_reset/$','login.views.into_reset'),
                       url(r'^reset/$','login.views.reset'),
                       
                       url(r'^logout/$', 'login.views.logout'),
                       
                       url(r'^go_reset/$', 'login.views.reset_page'),
                       url(r'^reset/$', 'login.views.reset'),
                       
                       url(r'^go_account/$', 'login.views.into_account'),
                       url(r'^list/$', 'login.views.list'),
                       url(r'^topic/$', 'login.views.topic'),
                       url(r'^opinion/$', 'login.views.opinion'),
                       url(r'^picture/$', 'login.views.picture'),
                       url(r'^ps/$', 'login.views.reset_ps'),
)
