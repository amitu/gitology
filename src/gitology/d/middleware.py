from django.utils import simplejson
from django import http 
from django.conf.urls.defaults import patterns
from django.conf import settings
from django.core import urlresolvers

import sys

from gitology.config import settings as gsettings
from gitology.d.views import show_post, show_wiki
from gitology import utils

class URLConfMiddleware:
    def __init__(self):
        self.cache_path = gsettings.LOCAL_REPO_PATH.joinpath("urlconf.cache")
        self.old_urlconf = utils.path2obj(settings.ROOT_URLCONF + ".urlpatterns")
        self.handler500 = utils.path2obj(settings.ROOT_URLCONF + ".handler500")
        self.handler404 = utils.path2obj(settings.ROOT_URLCONF + ".handler404")

    def _check_if_urlconf_valid(self):
        # see if _urlconf has been loaded at all
        if not hasattr(self, 'urlpatterns'):
            return False
        # if file has been modified after being loaded, its not valid
        if self.cache_path.getmtime() != self.cache_path_mtime:
            return False
        return True

    def _load_urlconf(self):
        self.urlpatterns = self.old_urlconf + patterns(
            *utils.refresh_urlconf_cache()
        )
        self.cache_path_mtime = self.cache_path.getmtime()
        sys.modules["gitology.d.urls"] = self

    def check_urlconf(self):
        # checks if the urlconf in memory is uptodate, else
        # loads it from disk
        if not self._check_if_urlconf_valid():
            self._load_urlconf()

    def process_request(self, request):
        self.check_urlconf()
        request.urlconf = "gitology.d.urls" # virtual module

    def process_response(self, request, response):
        if response.status_code != 404: return response
        if request.path in utils.global_blog_dict:
            return show_post(request)
        if request.path in utils.global_wiki_dict:
            return show_wiki(request)
        if request.path in utils.global_redirect_dict:
            return http.HttpResponsePermanentRedirect(
                utils.global_redirect_dict[request.path]
            )
        if not request.path.endswith("/"):
            if "%s/" % request.path in utils.global_blog_dict:
                return http.HttpResponsePermanentRedirect(request.path + "/")
            elif "." not in request.path.rsplit("/", 1)[-1]:
                try:
                    urlresolvers.resolve(
                        request.path_info
                    )
                except urlresolvers.Resolver404: 
                    return http.HttpResponseRedirect(request.path + "/")
                else:
                    return http.HttpResponsePermanentRedirect(
                        request.path + "/"
                    )
        return response # must be real 404!
