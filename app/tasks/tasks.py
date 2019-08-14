#!/usr/bin/python
#-*-coding:utf-8 -*-
from celery_app import celery
from app.config.sql import select_sql
from app.base.pythonProject.base.getCookies import get_cookies
import requests
import datetime
import json
@celery.task(bind=True)
def run_api(self,project):
    sql = """select project,case_api,case_host,case_url,method,params,headers,cookies,islogin,assertValue from case_http_api where project='%s' and scheduling='0'"""%(project)
    datas = select_sql(sql)
    datas_list = []
    keys = ["project","case_api","case_host","case_url","method","params","headers","cookies","islogin","assertValue"]
    for data in datas:
        key_value = dict(zip(keys,data))
        datas_list.append(key_value)

    case_total = len(datas_list) #全部用例
    current = 0  #计数器
    case_success = 0  #成功用例数
    case_mistake = 0  #代码错误用例数
    case_failed = 0  #失败用例数
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取开始时间
    ####获取project的Cookies
    ####pass
    ####
    for i in range(case_total):
        current += 1  # 计数器+1
        resp_status,resp_text = run_test(case_total[i])  # 传入 单条 接口用例数据
        case_api = case_total[i]["case_api"]  # 接口名称
        if resp_status:
            pass_status = 1
            case_success += 1
        elif resp_status == "mistake":
            pass_status = 0
            case_mistake += 1
        else:
            pass_status = 0
            case_failed += 1
    #   self.update_state(state='PROGRESS',
    #                       meta={'current': i, 'total': case_total,
    #                             'status': case_api,"pass_status":pass_status,"data_list":resp_text})
    # return {'current': current, 'total': case_total, 'status': u'执行成功!',
    #         'result': case_success}
def run_test(dict_datas):
    project = dict_datas["project"]  # 业务项目
    url = dict_datas["case_host"] + "/" + dict_datas["case_url"] # 请求连接
    method = dict_datas["method"]  # 请求方式
    params = dict_datas["params"]  # 请求参数
    headers = dict_datas["headers"]  # 请求头
    islogin = dict_datas["islogin"]  # 是否需要前置登录
    assertValue = dict_datas["assertValue"]  # 校验数据
    cookies = eval(dict_datas["cookies"])
    response = None  # 返回结果
    pass_status = None  # 测试结果
    if islogin:  # 判断需要登陆状态时，进行登录
        env_flag = cookies["env_flag"]
        env_num = cookies["env_num"]
        cookies = get_cookies(project,env_flag,env_flag,env_num)  # 更新cookies信息，变更为已登录
    try:
        if method.upper == "GET":
            resp = getFunction(url=url,headers=headers,params=params,cookies=cookies)
        else:
            resp = postFunction(url=url,headers=headers,data=params,cookies=cookies)
        dict_s = json.loads(resp.content,encoding="utf8")
        status_key_list = []  # 返回key + 验证结果
        status_list = []  # 返回验证结果boolean
        for key in dict_s.keys():
            keyf = None if "None" in key else key
            keyf_value = None if "None" in dict_s[key] else dict_s[key]
            sb = find_key(resp, keyf, keyf_value)
            wc = (key, sb)
            status_key_list.append(wc)
            status_list.append(sb)
        if False or None in status_list:
            return status_key_list,False
        else:
            return status_key_list,True



    return resp



def postFunction(url, params, headers, cookies):
    resp = requests.post(url, data=params, headers=headers, cookies=cookies)
    return resp.content

def getFunction(url, params, headers, cookies):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies)
    return resp.content







def find_key(resp,fkey,fvalue,resp_key=None):
    if isinstance(resp,dict):
        for key in resp.keys():
            if key==fkey and resp[key]==fvalue:
                return True
            else:
                resp_key = key
                s = find_key(resp[key],fkey,fvalue,resp_key)
                if s:
                    return True
    elif isinstance(resp,list) and fvalue!=None and fkey!=None:
        resp_list = resp
        for single in resp_list:
            b = find_key(single,fkey,fvalue,resp_key=None)
            if b:
                return True
    elif isinstance(resp,list) and fvalue==None:
        if fkey==resp_key:
            return True
    elif isinstance(resp,list) and fkey==None:
        if fvalue==resp:
            return True
    elif isinstance(resp,str) and fvalue!=None and fkey!=None:
        if resp_key==fkey and resp==fvalue:
            return True
    elif isinstance(resp,str) and fvalue==None:
        if resp_key==fkey:
            return True
    elif isinstance(resp,str) and fkey==None:
        if resp==fvalue:
            return True
    elif isinstance(resp,int) and fvalue!=None and fkey!=None:
        if resp_key==fkey and resp==fvalue:
            return True
    elif isinstance(resp,int) and fvalue==None:
        if resp_key==fkey:
            return True
    elif isinstance(resp,int) and fkey==None:
        if resp==fvalue:
            return True
    else:
        return False



if __name__ == "__main__":
    resp = {"a":"wctv","b":1,"c":["1","2"],"f":{"aa":"bb","aaa":[1,2,4],"d":"asdfasd"}}


    s = """{"aaa":[1,2,4],"d":"asdfasd"}"""
    dict_s = json.loads(s,encoding="utf-8")
    print s
    status_key_list = []
    status_list = []
    for key in dict_s.keys():
        keyf = None if "None" in key else key
        keyf_value = None if dict_s[key]=="None" else dict_s[key]
        sb = find_key(resp,keyf,keyf_value)
        wc = (key,sb)
        status_key_list.append(wc)
        status_list.append(sb)
    print status_key_list,status_list
























