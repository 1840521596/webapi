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
    sql = """select project,case_api,case_host,case_url,method,params,headers,cookies,islogin,assertValue from case_http_api where project='%s' and scheduling='1'"""%(project)
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
        status_key_list,resp_status,resp_text = run_test(datas_list[i])  # 传入 单条 接口用例数据
        print status_key_list
        print type(resp_status)
        print resp_text
        case_api = datas_list[i]["case_api"]  # 接口名称
        if resp_status =="True":
            pass_status = 1
            case_success += 1
        elif resp_status == "Mistake":
            pass_status = 0
            case_mistake += 1
        else:
            pass_status = 0
            case_failed += 1
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': case_total,
                                'status': case_api,"pass_status":pass_status,"data_list":resp_text})
    #print str(case_success) + "----" + str(case_failed) + "----" + str(case_mistake)
    with open("wctv.log","a+") as f:
        f.write("wctv\n")
    return {'current': current, 'total': case_total, 'status': u'执行成功!','result': case_success,"case_failed":case_failed,"case_mistake":case_mistake}
def run_test(dict_datas):
    project = dict_datas["project"]  # 业务项目
    url = dict_datas["case_host"] + "/" + dict_datas["case_url"] # 请求连接
    method = dict_datas["method"]  # 请求方式
    params = eval(dict_datas["params"])  # 请求参数
    headers = eval(dict_datas["headers"])  # 请求头
    islogin = dict_datas["islogin"]  # 是否需要前置登录
    assertValue_dict = None if dict_datas["assertValue"]=="None" else json.loads(dict_datas["assertValue"],encoding="utf8") # 校验数据
    cookies = eval(dict_datas["cookies"])
    if islogin:  # 判断需要登陆状态时，进行登录
        env_flag = cookies["env_flag"]
        env_num = cookies["env_num"]
        sql = """select project_en from project_api where project='%s';""" % (project)
        project_en = select_sql(sql)[0][0]  # 获取项目名称
        cookies = get_cookies(project_en,env_flag,env_num)  # 更新cookies信息，变更为已登录
    try:
        if method.upper == "GET":
            resp = getFunction(url=url,headers=headers,params=params,cookies=cookies)
        else:
            resp = postFunction(url=url,headers=headers,params=params,cookies=cookies)
        resp_dict_s = json.loads(resp.content,encoding="utf8")
        status_key_list = []  # 返回key + 验证结果
        status_list = []  # 返回验证结果boolean
        if assertValue_dict==None:
            pass_status = "True"
            return status_key_list,pass_status,resp.content
        else:
            for key in assertValue_dict.keys():
                keyf = None if "None" in key else key
                keyf_value = None if "None" in assertValue_dict[key] else assertValue_dict[key]
                sb = find_key(resp_dict_s, keyf, keyf_value)
                status_key_list.append((key, sb))
                status_list.append(sb)
            if False or None in status_list:
                pass_status = "False"
                return status_key_list,pass_status,resp.content
            else:
                pass_status = "True"
                return status_key_list,pass_status,resp.content
    except Exception as e:
        status_key_list = []
        pass_status = "Mistake"
        return status_key_list,pass_status,str(e)



def postFunction(url, params, headers, cookies):
    resp = requests.post(url, data=params, headers=headers, cookies=cookies)
    return resp

def getFunction(url, params, headers, cookies):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies)
    return resp

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

def make_html_report():
    html_table = """<table id = "progressing_2" class ="table table-striped table-bordered table-hover" > < tbody > < tr > < th width="10%" class ="btn-info" > 接口名称 < / th > < th width="20%" class ="btn-info" > URL < / th > < th width="5%" class ="btn-info" > 请求方式 < / th > < th width="30%" class ="btn-info" > 返回结果 < / th > < th width="30%" class ="btn-info" > 预期结果 < / th > < th width="5%" class ="btn-info" > 测试结果 < / th > < / tr > < / tbody > < tbody id="casetb_2" > < / tbody > < / table >"""
    

if __name__ == "__main__":
    run_api("wc","云舒写首页")
























