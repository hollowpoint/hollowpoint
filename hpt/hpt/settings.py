"""
Django settings for hpt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q&u@06$33br&__fo4ia=dg#&)vl0u*s(&md7$1&qez*xh48m*r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'djcelery',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hpt.urls'

WSGI_APPLICATION = 'hpt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hpt',
        'USER': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

################
# Celery Stuff #
################
# http://celery.readthedocs.org/en/latest/configuration.html

# Broker settings.
BROKER_URL = 'amqp://admin:admin@hpt.local:5672//'

# Use SSL to connect to the broker. Off by default. This may not be supported by
# all transports.
#BROKER_USE_SSL = True
BROKER_USE_SSL = False

# A dict of additional options passed to the underlying transport.
# See: http://kombu.readthedocs.org/en/latest/reference/kombu.connection.html
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SSL_DIR = os.path.join(PROJECT_ROOT, 'ssl')
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
#CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
#CELERY_TIMEZONE = 'America/Los_Angeles'
#CELERY_ENABLE_UTC = True

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
    'api.tasks.add': {
        'queue': 'math',
        'routing_key': 'math.add',
    },
    'api.tasks.mul': {
        'queue': 'math',
        'routing_key': 'math.mul',
    },
    'api.tasks.xsum': {
        'queue': 'math',
        'routing_key': 'math.xsum',
    },
    'api.tasks.execute_commands': {
        'queue': 'commands',
        'routing_key': 'commands.execute',
    },
}
"""
