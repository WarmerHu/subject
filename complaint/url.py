#coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^add/$', 'complaint.views.add'),
    url(r'^cancel/$', 'complaint.views.cancel'),
    url(r'^individual/me/$', 'complaint.views.get_myComplaint'),
    url(r'^individual/me/from/$', 'complaint.views.get_complaintFromMe'),
    url(r'^individual/$', 'complaint.views.into_complaint'),
)
