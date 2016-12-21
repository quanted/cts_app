"""
Django settings for UberDjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os, sys
import socket
#import secret

# Get machine IP address
MACHINE_ID = socket.gethostname()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Boolean for if it's on Nick's local machine or not..
NICK_LOCAL = False

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'UBERTOOL_BATCH_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com/',
    'UBERTOOL_MONGO_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com',
    'UBERTOOL_SECURE_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com',   
    'UBERTOOL_REST_SERVER': 'http://172.20.100.15:7777',        # CGI Internal
    'CTS_TEST_SERVER': 'http://172.20.100.16:8080',                   # test rest server (intranet)
    'CTS_JCHEM_SERVER': 'http://172.20.100.12',       # jchem rest server (internal)
    # 'CTS_EPI_SERVER': 'http://172.20.100.16:7080',
    'CTS_EPI_SERVER': 'http://172.20.100.18',
    'CTS_EFS_SERVER': 'http://172.20.100.12',
    'CTS_SPARC_SERVER': 'http://204.46.160.69:8080',         # SPARC rest server (external)
    'wkhtmltopdf': PROJECT_ROOT + '/wkhtmltopdf/linux/wkhtmltopdf',
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': '',                          # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CTS_VERSION': '1.4.7'
})

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wx$p52y!1p!*p$$y^d!f9@5=)3o#88+08-i9_mc8*-8h+x2&@w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []
if MACHINE_ID == "ord-uber-vm001":
    ALLOWED_HOSTS.append('134.67.114.1')
    ALLOWED_HOSTS.append('qedinternal.epa.gov')
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')
elif MACHINE_ID == "ord-uber-vm003":
    ALLOWED_HOSTS.append('134.67.114.3')
    ALLOWED_HOSTS.append('qed.epa.gov')
else:
    ALLOWED_HOSTS.append('192.168.99.100')
    ALLOWED_HOSTS.append('134.67.114.7')
    ALLOWED_HOSTS.append('*')  # This forces Django to serve behind NGINX when "DEBUG = False"

# # celery config stuff:
# CELERY_RESULT_BACKEND = 'redis://'
# # CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'redis//'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'


APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'mod_wsgi.server',
    'filters',
    # 'epi_cts',
    # 'celery_cts',
    #'test_cts'
    #'docs',
    'cts_api',
    'cts_testing'
)

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi_apache.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Setups databse-less test runner (Only needed for running test)
TEST_RUNNER = 'testing.DatabaselessTestRunner'

# CACHE Setup - required to run Django "sessions" without a database

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = '/src/collected_static/'

# print 'BASE_DIR = %s' %BASE_DIR
# print 'PROJECT_ROOT = %s' %PROJECT_ROOT

# Path to Sphinx HTML Docs
# http://django-docs.readthedocs.org/en/latest/

DOCS_ROOT = os.path.join(PROJECT_ROOT, 'docs', '_build', 'html')

DOCS_ACCESS = 'public'

# NODEJS_HOST = '134.67.114.1'
NODEJS_HOST = 'nginx'
NODEJS_PORT = 80


try:
    # override any settings unique to local machine
    from settings_local import *
except ImportError as e:
    pass