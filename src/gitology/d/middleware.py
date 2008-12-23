from django.utils import simplejson
from django.conf.urls.defaults import patterns
from django.conf import settings

import sys

from gitology.config import settings as gsettings
from gitology import utils

class URLConfMiddleware:
    def __init__(self):
        self.cache_path = gsettings.LOCAL_REPO_PATH.joinpath("urlconf.cache")
        self.old_urlconf = utils.path2obj(settings.ROOT_URLCONF + ".urlpatterns")

    def _check_if_urlconf_valid(self):
        # see if _urlconf has been loaded at all
        if not hasattr(self, '_urlconf'):
            return False
        # if file has been modified after being loaded, its not valid
        if self.cache_path.getmtime() != self.cache_path_mtime:
            return False
        return True

    def _load_urlconf(self):
        self.urlpatterns = self.old_urlconf + patterns(
            *simplejson.loads(file(self.cache_path).read())
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
