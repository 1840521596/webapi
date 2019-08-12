#!/usr/bin/python
from celery import Celery
celery = Celery('celery_app',
broker='redis://localhost:6379/1',
backend='redis://localhost:6379/2')
