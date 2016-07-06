#!/bin/bash

#REQUESTS_CA_BUNDLE=/etc/rabbitmq/ssl/ca/cacert.pem python hpt/manage.py celery flower --address=0.0.0.0 --certfile=/etc/rabbitmq/ssl/server/server.cert.pem --keyfile=/etc/rabbitmq/ssl/server/server.key.pem --broker-api="https://admin:admin@localhost:15672/api/" --persistent

# Basic Auth
#python hpt/manage.py celery flower --address=0.0.0.0 --broker-api="http://admin:admin@localhost:15672/api/" --persistent --basic_auth=admin:admin

# No auth
# python hpt/manage.py celery flower --address=0.0.0.0 --broker-api="http://admin:admin@localhost:15672/api/" --persistent
# python hpt/manage.py celery flower --address=0.0.0.0 --broker-api="http://guest:guest@192.168.33.10:15672/api/" --persistent
# python hpt/manage.py celery flower --address=0.0.0.0 --persistent
python hpt/manage.py celery flower --address=0.0.0.0
