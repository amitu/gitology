from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'.*', 'gitology.d.resolver.resolve'),
)
