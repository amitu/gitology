# Django settings for web project.
import path

SETTINGS_FILE_FOLDER = path.path(__file__).parent

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Amit Upadhyay', 'gitology@amitu.com'),
)

MANAGERS = ADMINS

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Chicago'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SECRET_KEY = 'qrz%q1z(%z+%!h3eq&l6qadwc+^wt3x(i8ntirvdmxnsdwgrvr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_openidconsumer.middleware.OpenIDMiddleware',

    'gitology.d.middleware.URLConfMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django.core.context_processors.media',
    'django.core.context_processors.request'
)

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
RECAPTCHA_PUB_KEY = "YOUR PUBLIC KEY"
RECAPTCHA_PRIV_KEY = "YOUR SECRET KEY"
RECAPTCHA_THEME = "white"
# }}}

try:
    from local_settings import *
except ImportError: pass

