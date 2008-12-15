from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (   
        # some url not managed by gitology. 
        # gitology will add to this conf file for the rest of the urls.
        'about/$', 'django.views.generic.simple.direct_to_template',
        { 'template': 'website/about.html' },
    ),
)
