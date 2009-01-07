from django.conf.urls.defaults import *

from gitology.config import settings as gsettings
from gitology.d import urls as gitology_urls

urlpatterns = patterns('',
    # some url not managed by gitology. 
    # gitology will add to this conf file for the rest of the urls.
    (   
        'files/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': gsettings.LOCAL_REPO_PATH.joinpath("files") },
    ),
    (   
        'static/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': gsettings.LOCAL_REPO_PATH.joinpath("static") },
    ),
)

urlpatterns += gitology_urls.urlpatterns
