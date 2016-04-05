from django.conf.urls import patterns, include, url

from django.contrib import admin
import login.urls
import exercise.url
import collection.urls
import resources.urls
from subject import settings
import activity.urls
import fortune.urls
import bbs.urls
import jobs.urls
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'subject.views.home', name='home'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include(login.urls)),
    url(r'^title/', include(exercise.url)),
    url(r'^collection/', include(collection.urls)),
    url(r'^resources/', include(resources.urls)),
    url(r'^activity/', include(activity.urls)),
    url(r'^fortune/', include(fortune.urls)),
    url(r'^bbs/', include(bbs.urls)),
    url(r'^jobs/', include(jobs.urls)),
    url(r'^$', 'login.views.index'),
)
