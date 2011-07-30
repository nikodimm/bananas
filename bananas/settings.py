# -*- coding: utf-8 -*-
import os, sys

#####################################################################
# Project path and environment set-up

PROJECT_ROOT = os.path.abspath(
        os.path.dirname(__file__))

LIBS = (
    # tuple for path, where each element is an element of tuple 
    # libs/django -> ('django',) 
    # libs/foo/bar -> ('foo', 'bar')
)

# add third-party libs to sys.path 
for lib in LIBS:
    libdir = os.path.join(PROJECT_ROOT, 'libs', *lib)
    if os.path.isdir(libdir) and libdir not in sys.path:
        sys.path.insert(0, libdir)

# add apps to sys.path 
appdir = os.path.join(PROJECT_ROOT, 'apps')
if appdir not in sys.path:
    sys.path.insert(0, appdir)

#####################################################################
DEBUG = not os.path.exists(os.path.join(PROJECT_ROOT, 'release'))
TEMPLATE_DEBUG = DEBUG
SOUTH_TESTS_MIGRATE=False
#####################################################################
ADMINS = (
    ('Mikhail Podgursliy', 'kmmbvnr@gmail.com'),
)
MANAGERS = ADMINS

#####################################################################
SITE_ID = 1
TIME_ZONE = 'US/Pacific'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
ROOT_URLCONF = 'urls'
APPEND_SLASH = True
REMOVE_WWW = True

DATE_INPUT_FORMATS = ('%Y-%m-%d', )

DATETIME_INPUT_FORMATS = ('%Y-%m-%d %I:%M %p', )

DATETIME_FORMAT = "Y-m-d h:i A"
SHORT_DATETIME_FORMAT = "Y-m-d h:i A"

LANGUAGES = [
    ('en', 'English'),
]

PROJECT_APPS = (
    'website',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
) + PROJECT_APPS

#####################################################################
FIXTURE_DIRS = [os.path.join(PROJECT_ROOT, 'fixtures')]

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

CACHE_BACKEND = 'locmem://'
CACHE_PREFIX = 'bananas-'

#####################################################################
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

LOGIN_REDIRECT_URL = '/'

#####################################################################
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages'    
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

#####################################################################
#   There settings need to be overriden in production environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '..', 'dev.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

#####################################################################
# Allow override default settings
try:
    from settings_local import *
except ImportError:
    pass

#####################################################################
# Hooks and preinitialisation code
if not hasattr(globals(), 'SECRET_KEY'):
    # Make this unique, and don't share it with anybody.
    # Don't share it with anybody 
    SECRET_FILE = os.path.join(PROJECT_ROOT, '..', 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            SECRET_KEY = ''.join([
                choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters '
                            'to generate your secret key!' % SECRET_FILE)
