#!/bin/bash
rm celery.log;
rm uwsgi.log;
celery -A  manage.celery worker --loglevel=info > celery.log &;
uwsgi uwsgi.init;
exit;
