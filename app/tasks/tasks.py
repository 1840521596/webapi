#!/usr/bin/python
#-*-coding:utf-8 -*-
from celery_app import celery
from ..config.sql import select_sql
import requests
import datetime
import time
import random
@celery.task(bind=True)
def run_api(self,project):
    sql = """select project,case_api,case_host,case_url,method,params,headers,cookies,assertValue from case_http_api where project='%s' and scheduling='0'"""%(project)
    datas = select_sql(sql)
    datas_list = []
    keys = ["project","case_api","case_host","case_url","method","params","headers","cookies","assertValue"]
    for data in datas:
        key_value = dict(zip(keys,data))
        datas_list.append(key_value)
    case_total = len(datas_list) #全部用例
    case_success = 0  #成功用例
    case_failed = 0  #失败用例数
    current = 0 # 计数器
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取开始时间
    ####获取project的Cookies
    ####pass
    ####
    for i in range(case_total):
        current += 1
        pass_status = random.randint(0, 1)

        case_api = datas_list[i]["case_api"]
        resp = "resp%d"%(current)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': case_total,
                                'status': case_api+"%d"%(i),"pass_status":pass_status,"data_list":datas_list[i],"resp":resp})
        time.sleep(1)
    return {'current': current, 'total': case_total, 'status': u'执行成功!',
            'result': case_success}