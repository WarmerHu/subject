from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$','django.views.static.serve',),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'exercise.views.index'),
    url(r'^title$', 'exercise.views.into_title'),
    url(r'^elist/(.+)/$', 'exercise.views.get_title'),
    url(r'^elist/$', 'exercise.views.check_answer'),
)
