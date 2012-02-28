# Django settings for cracket project.
import os

DEV = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('@JCeb', 'julian@pikhub.com'),
)

MANAGERS = ADMINS

PROJECT_DIR = '/home/dotcloud'
URL = 'http://cracket-rbfve6jh.dotcloud.com'

path = lambda *args: os.path.join(PROJECT_DIR, *args)

if DEV:
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    URL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path('db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

if not DEV:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': path('data','db.sqlite'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'es'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = path('media')

if not DEV:
    MEDIA_ROOT = path('data','media')

MEDIA_URL = URL+'/medios'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'lf+0=shw$2sm^-tbc%oz_t6ljwfz-5-8a9_j24(f^@q1-p@okj'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    path('current','templates'),
)

if DEV:
    TEMPLATE_DIRS = (
        path('templates'),
    )

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.admin',
    'institutes',
    'characters',
    'comments',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'context_processors.default',
)
