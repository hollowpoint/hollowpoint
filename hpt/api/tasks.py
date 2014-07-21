from __future__ import absolute_import
from celery import shared_task
import os


@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def ping():
    return 'PONG'

TRIGGER_HOST = os.getenv('TRIGGER_HOST')
if TRIGGER_HOST is None:
    raise RuntimeError('You must define TRIGGER_HOST')
import xmlrpclib

client = xmlrpclib.Server('https://%s:9000/' % TRIGGER_HOST)

@shared_task
def execute_commands(*args, **kwargs):
    result = client.execute_commands(args, kwargs)
    return result

@shared_task
def change_passwords(*args, **kwargs):
    result = client.change_passwords(args, kwargs)
    return result

"""
@shared_task
def trigger_add(x, y):
    client = xmlrpclib.Server('https://%S:9000/' % TRIGGER_HOST)
    result = client.add(x, y)
    return result
"""
