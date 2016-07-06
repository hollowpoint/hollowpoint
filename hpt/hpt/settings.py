"""
Django settings for hpt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import socket


#############
# Directories
#############
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# e.g. /path/to/hollowpoint/hpt/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# e.g. /path/to/hollowpoint
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# e.g. /path/to/hollowpoint/hpt/hpt
SETTINGS_ROOT = os.path.abspath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q&u@06$33br&__fo4ia=dg#&)vl0u*s(&md7$1&qez*xh48m*r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = ['*']


########################
# Application definition
########################

INSTALLED_APPS = (
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Debug Toolbar
    #'debug_toolbar',

    # Server stuff
    # 'xadmin',
    # 'south',
    # 'crispy_forms',
    # 'reversion',

    # Application stuff
    'overextends',
    'rest_framework',
    'django_extensions',
    'djcelery',

    # Plugins
    'core',
    'inventory',
    'acls',
)

# Note for caching to work the explicit ordering of the CacheMiddleware must be
# maintained.
# TODO(jathan): Revisit this to turn caching middleware back on.
"""
MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware', # This must be first!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # This must be last!
]
"""
MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware', # This must be first!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # This must be last!
]

ROOT_URLCONF = 'hpt.urls'

WSGI_APPLICATION = 'hpt.wsgi.application'

##########
# Database
##########
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# This should be overridden in local_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hpt',
        'USER': 'postgres',
        # 'HOST': '192.168.33.10',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Parse database configuration from $DATABASE_URL
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

######################
# Internationalization
######################
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


##############
# Static files (CSS, JavaScript, Images)
##############
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

########
# Celery
########
# http://celery.readthedocs.org/en/latest/configuration.html

# Broker settings.
#BROKER_URL = 'amqp://admin:admin@localhost:5672//'
#BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# BROKER_URL = 'amqp://guest:guest@192.168.33.10:5672/'
BROKER_URL = 'redis://localhost:6379/1'

# Use SSL to connect to the broker. Off by default. This may not be supported by
# all transports.
#BROKER_USE_SSL = True
BROKER_USE_SSL = False

# A dict of additional options passed to the underlying transport.
# See: http://kombu.readthedocs.org/en/latest/reference/kombu.connection.html
SSL_DIR = os.path.join(PROJECT_ROOT, 'configs/ssl')
FQDN = socket.getfqdn()
"""
BROKER_TRANSPORT_OPTIONS = {
    'ssl': {
        'ca_certs': os.path.join(SSL_DIR, 'ca/cacert.pem'),
        'certfile': os.path.join(SSL_DIR, 'client/%s.cert.pem' % FQDN),
        'keyfile': os.path.join(SSL_DIR, 'client/%s.key.pem' % FQDN),
    }
}
"""

# Set custom amqp login method, default is AMQPLAIN. This forces SSL certificate
# authentication based on the CN (hostname) baked into the client certificate
# specified above in BROKER_TRANSPORT_OPTIONS.
#BROKER_LOGIN_METHOD = 'EXTERNAL'

# If enabled dates and times in messages will be converted to use the UTC
# timezone. Enabled by default since version 3.0.
#CELERY_ENABLE_UTC = True

# Use amqp to store results
#CELERY_RESULT_BACKEND = 'amqp'
# Configure celery to use the django-celery backend
# See: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-django-orm-cache-as-a-result-backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# How long until results expire
#CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.
CELERY_TASK_RESULT_EXPIRES = None # Never

# If set to True, result messages will be persistent. This means the messages
# will not be lost after a broker restart. The default is for the results to be
# transient.
CELERY_RESULT_PERSISTENT = True

# If True the task will report its status as "started" when the task is executed
# by a worker.
CELERY_TRACK_STARTED = True

# Send events so the worker can be monitored by tools like celerymon.
CELERY_SEND_EVENTS = True

# If enabled, a task-sent event will be sent for every task so tasks can be
# tracked before they are consumed by a worker.
CELERY_SEND_TASK_SENT_EVENT = True

# By default monitor data for successful tasks will expire in 1 day, failed
# tasks in 3 days and pending tasks in 5 days. You can change the expiry times
# for each of these using adding the following settings to your settings.py:
"""
from datetime import timedelta

CELERYCAM_EXPIRE_SUCCESS = timedelta(days=1)
CELERYCAM_EXPIRE_ERROR = timedelta(days=3)
CELERYCAM_EXPIRE_PENDING = timedelta(days=5)
"""
CELERYCAM_EXPIRE_SUCCESS = None   # Never expire
CELERYCAM_EXPIRE_ERROR = None     # Never expire
CELERYCAM_EXPIRE_PENDING = None   # Never expire

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
#CELERY_TIMEZONE = 'America/Los_Angeles'
#CELERY_ENABLE_UTC = True

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']

# The mapping of queues the worker consumes from. This is a dictionary of queue
# name/options.
"""
CELERY_QUEUES = {
    'default': {
        'exchange': 'hpt',
        'exchange_type': 'topic',
        'binding_key': 'task.#',
    },
    'commands': {
        'exchange': 'hpt',
        'exchange_type': 'topic',
        'binding_key': 'commands.#',
    },
    'math': {
        'exchange': 'hpt',
        'exchange_type': 'topic',
        'binding_key': 'math.#',
    },
}
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'hpt'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

# This will set the default HA policy for a queue, and the value can either be a
# string (usually all).
CELERY_QUEUE_HA_POLICY = 'all'

# If enabled (default), any queues specified that are not defined in
# CELERY_QUEUES will be automatically created.
CELERY_CREATE_MISSING_QUEUES = True

# Default exchange type used when no custom exchange type is specified for a key
# in the CELERY_QUEUES setting. The default is: direct.
CELERY_ROUTES = {
    'core.tasks.add': {
        'queue': 'math',
        'routing_key': 'math.add',
    },
    'core.tasks.mul': {
        'queue': 'math',
        'routing_key': 'math.mul',
    },
    'core.tasks.xsum': {
        'queue': 'math',
        'routing_key': 'math.xsum',
    },
    'core.tasks.execute_commands': {
        'queue': 'commands',
        'routing_key': 'commands.execute',
    },
}
"""

#############
# Look & Feel
#############
XADMIN_SITE_NAME = 'Hollowpoint'
XADMIN_SITE_TITLE = '<img src="/static/img/logo.png" alt="Hollowpoint" width="140">'
XADMIN_SITE_FOOTER = 'Hollowpoint Technology Group, Inc.'

###########
# Templates
###########

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SETTINGS_ROOT, "templates").replace('\\', '/'),
        ],
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

# Logging
from django.conf.global_settings import LOGGING
LOGGING['version'] = 1

##########
# Sessions
##########

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_PREFIX = 'session'

SESSION_COOKIE_NAME = 'hpt'

########
# Caches
########
# Setup REdis to store cache data (instead of memcached)
# For more advanced setup:
# http://michal.karzynski.pl/blog/2013/07/14/using-redis-as-django-session-store-and-cache-backend/
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        # 'LOCATION': '192.168.33.10:6379',
        'OPTIONS': {
            'DB': 2,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
        },
    },
}

# Disable cache if we're debugging
# http://stackoverflow.com/a/7603746/194311
if DEBUG:
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

################
# REST Framework
################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'limit', # Override, using `?limit=xxx`
    'MAX_PAGINATE_BY': None,          # Max limit, None disables it
}

#########
# Trigger
#########
TRIGGER_SETTINGS = '/home/jathan/.trigger/settings.py'
os.environ['TRIGGER_SETTINGS'] = TRIGGER_SETTINGS

################
# Local settings
################
try:
    from local_settings import *
except ImportError as err:
    print 'Could not load local_settings.py:', err
    pass
