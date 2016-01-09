from django.conf.urls import patterns, include, url

from django.contrib import admin
import login.urls
import exercise.url
import collection.urls
import resources.urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'subject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$','django.views.static.serve',),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include(login.urls)),
    url(r'^title/', include(exercise.url)),
    url(r'^collection/', include(collection.urls)),
    url(r'^resources/', include(resources.urls)),
    url(r'^$', 'exercise.views.index'),
)
