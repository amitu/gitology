# imports
from django.conf import settings

from gitology.config import settings as gsettings

# context_processor # {{{
def context_processor(request):
    return { 'LOCAL_INSTANCE': getattr(settings, 'LOCAL_INSTANCE', False) }
# }}}

# select_theme # {{{
def select_theme(view_func):
    def wrapped(request, *args, **kw):
        if request.GET.get("theme"):
            gsettings.threadlocal.theme = request.GET["theme"]
        elif "THEME" in gsettings.DEFAULTS:
            gsettings.threadlocal.theme = gsettings.DEFAULTS.THEME
        return view_func(request, *args, **kw)
    wrapped.__doc__ = view_func.__doc__
    wrapped.__dict__ = view_func.__dict__
    return wrapped
# }}}
