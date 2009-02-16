from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^openid/$', 'django_openidconsumer.views.begin'),
    (r'^openid/with-sreg/$', 'django_openidconsumer.views.begin', {
        'sreg': 'email',
        'redirect_to': '/openid/complete/',
    }),
    (r'^openid/complete/$', 'django_openidconsumer.views.complete'),
    (r'^openid/signout/$', 'django_openidconsumer.views.signout'),
    (r'^document/(?P<name>.*)/$', 'gitology.d.views.show_document'),
)
