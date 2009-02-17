from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'django_openidconsumer.views.begin'),
    (r'^login/with-sreg/$', 'django_openidconsumer.views.begin', {
        'sreg': 'email',
        'redirect_to': '/login/complete/',
    }),
    (r'^login/complete/$', 'django_openidconsumer.views.complete'),
    (r'^logout/$', 'django_openidconsumer.views.signout'),
    (r'^document/(?P<name>.*)/$', 'gitology.d.views.show_document'),
)
