#!/usr/bin/python
#-*-coding:utf-8 -*-
from celery_app import celery
import time
@celery.task(bind=True)
def main_task(self, task_flag):
    print(task_flag + " app.main.task start")
    for i in range(10):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': 10,
                                'status': "sleeping"})
        print(i)
        time.sleep(1)
    print(task_flag + " app.main.task end")
    return {'current': 100, 'total': 100, 'status': 'awake!',
            'result': "done!"}
@celery.task()
def wctvb(msg):
    with open("wctv.log","a+") as f:
        f.write(msg)
    return "wctvb"