#!/bin/bash

REQUESTS_CA_BUNDLE=/etc/rabbitmq/ssl/ca/cacert.pem python hpt/manage.py celery flower --address=0.0.0.0 --certfile=/etc/rabbitmq/ssl/server/server.cert.pem --keyfile=/etc/rabbitmq/ssl/server/server.key.pem --broker-api="https://admin:admin@hpt.local:15672/api/" --persistent
