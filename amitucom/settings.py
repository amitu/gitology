# Django settings for web project.

# relocatable django # {{{
import path
SETTINGS_FILE_FOLDER = path.path(__file__).parent
# }}}

# DEBUG # {{{
DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG
#TEMPLATE_DEBUG = False
# }}}

# ADMINS etc # {{{
ADMINS = (
    ('Amit Upadhyay', 'gitology@amitu.com'),
)

MANAGERS = ADMINS
# }}}

# Mail settings # {{{
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = "[amitu.com] "
# }}}

# Django Internal # {{{
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Chicago'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SECRET_KEY = 'qrz%q1z(%z+%!h3eq&l6qadwc+^wt3x(i8ntirvdmxnsdwgrvr'
APPEND_SLASH = True
# }}}

# MIDDLEWARE_CLASSES # {{{
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_openidconsumer.middleware.OpenIDMiddleware',

    'gitology.d.middleware.URLConfMiddleware',
)
# }}}

# TEMPLATE_LOADERS # {{{
TEMPLATE_LOADERS = (
    'gitology.d.themed_template_loader.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
# }}}

# TEMPLATE_CONTEXT_PROCESSORS # {{{
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django.core.context_processors.media',
    'django.core.context_processors.request',

    'gitology.d.utils.context_processor',
)
# }}}

ROOT_URLCONF = 'amitucom.urls'

from gitology.config import settings as gsettings

TEMPLATE_DIRS = (
    gsettings.LOCAL_REPO_PATH.joinpath("templates"),
)

DATABASE_ENGINE = "sqlite3"
DATABASE_NAME = "sqlite.db"

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django_openidconsumer',

    'gitology.d',
)

# recaptcha # {{{
RECAPTCHA_PUB_KEY = "YOUR RECAPTHCA PULIC KEY"
RECAPTCHA_PRIV_KEY = "YOUR RECAPTHCA PRIVATE KEY"
RECAPTCHA_THEME = "white"
# }}}

LOCAL_INSTANCE = False

# local_settings # {{{
try:
    from local_settings import *
except ImportError: pass
# }}}
