from django.conf.urls import patterns, include, url

from django.contrib import admin
import login.urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$','django.views.static.serve',),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include(login.urls)),
    url(r'^title$', 'exercise.views.into_title'),
    url(r'^elist/(.+)/$', 'exercise.views.get_title'),
    url(r'^elist/$', 'exercise.views.check_answer'),
    url(r'^$', 'exercise.views.index'),
)
