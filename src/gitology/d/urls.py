from django.conf.urls.defaults import patterns

urlpatterns = patterns('gitology.d.resolver',
    ('^(?P<document>.*)/$', 'resolve'),
)
