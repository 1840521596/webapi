#!/usr/bin/python
#-*-coding:utf-8
from flask import Flask
from flask_celery import Celery
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
celery = Celery(app)
@celery.task()
def wctv(wctva):
    return wctva
if __name__ == "__main__":
    result = wctv("wctv")
    print result.get()
