from django.conf import settings

from gitology.config import settings as gsettings

# context_processor # {{{
def context_processor(request):
    d = { 
        'LOCAL_INSTANCE': getattr(settings, 'LOCAL_INSTANCE', False) 
    }
    if "THEME" in gsettings.DEFAULTS:
        d["THEME"] = "%s/" % gsettings.DEFAULTS.THEME
    else:
        d["THEME"] = ""
    return d
# }}}
