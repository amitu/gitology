from django.utils import simplejson
from django.conf import settings

class URLConfMiddleware:
    def __init__(self):
        self.cache_path = settings.GITOLOGY_REPO.joinpath("urlconf.cache")

    def _check_if_urlconf_valid(self):
        # see if _urlconf has been loaded at all
        if not hasattr(self, '_urlconf'):
            return False
        # if file has been modified after being loaded, its not valid
        if self.cache_path.getmtime() != self.cache_path_mtime:
            return False
        return True

    def _load_urlconf(self):
        self._urlconf = settings.ROOT_URLCONF + simplejson.load(
            file(self.cache_path)
        )
        self.cache_path_mtime = self.cache_path.getmtime()

    def get_urlconf(self):
        # checks if the urlconf in memory is uptodate, else
        # loads it from disk
        if not self._check_if_urlconf_valid():
            self._load_urlconf()
        return self._urlconf

    def process_request(self, request):
        request.urlconf = self.get_urlconf()
