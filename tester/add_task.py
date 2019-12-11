#-*-coding:utf-8 -*-
import time
from collections import OrderedDict
from celery_app_task import add
result = add.delay()
a = {1:"wc",3:"wd",2:"ww"}
w = OrderedDict(a.items())
for m,value in w.items():
    print m,value