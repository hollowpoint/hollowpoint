#!/bin/bash
TRIGGER_HOST=pixel.local python hpt/manage.py celery worker -l info
