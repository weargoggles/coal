from django.conf.urls.defaults import patterns, include, url
import coal.views

urlpatterns = patterns(
    '',
    url(r'^$', coal.views.root),
    url(r'^hosts/([^/]+)/$', coal.views.host),
)