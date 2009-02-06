from django.conf import settings

# context_processor # {{{
def context_processor(request):
    return { 'LOCAL_INSTANCE': settings.LOCAL_INSTANCE }
# }}}
