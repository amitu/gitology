from django.conf import settings

# context_processor # {{{
def context_processor(request):
    return { 'LOCAL_INSTANCE': getattr(settings, 'LOCAL_INSTANCE', False) }
# }}}
