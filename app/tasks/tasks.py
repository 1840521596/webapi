#!/usr/bin/python
#-*-coding:utf-8 -*-
from celery_app import celery
from app.config.sql import select_sql
from app.config.html_template import test_case_detailed,html_all
from app.base.pythonProject.base.getCookies import get_cookies
import requests
import datetime
import json
import os


@celery.task(bind=True)
def run_api(self,project,developer,cookies):
    html_test_msg = ""
    sql = """select project,case_api,case_host,case_url,method,params,headers,islogin,assertValue,account from case_http_api where project='%s' and scheduling='1'"""%(project)
    datas = select_sql(sql)
    datas_list = []
    keys = ["project","case_api","case_host","case_url","method","params","headers","islogin","assertValue","account"]
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
        case_api = datas_list[i]["case_api"]  # 接口名称
        case_url = datas_list[i]["case_host"] + datas_list[i]["case_url"]
        case_params = datas_list[i]["params"]
        assertValue = datas_list[i]["assertValue"]
        status_key_list,resp_status,resp_text = run_test(datas_list[i],cookies)  # 传入 单条 接口用例数据
        print status_key_list
        print resp_status
        print resp_text
        if resp_status =="True":
            pass_status = 1
            case_success += 1
        elif resp_status == "Mistake":
            pass_status = 2
            case_mistake += 1
        else:
            pass_status = 0
            case_failed += 1
        api_name = case_api  #"接口名称"
        api_url =  case_url  #"接口链接"
        request_params = case_params  #"请求参数"
        assertValue = assertValue  #"校验参数"
        responce_params = resp_text  #"返回参数"
        method = datas_list[i]["method"]
        project_cn = datas_list[i]["project"]
        if pass_status == 1:
            status_color = "btn-success"
            case_status = u"通过"
        elif pass_status==0:
            status_color = "btn-danger"
            case_status = u"失败"
        else:
            status_color = "btn-danger"
            case_status = u"返回错误"
        new_detailed = test_case_detailed.format(api_name=api_name, method=method, api_url=api_url,
                                                 request_params=request_params, assertValue=assertValue,
                                                 status_color=status_color, case_status=case_status,
                                                 responce_params=responce_params,pid=str(i))
        html_test_msg += new_detailed
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': case_total,
                               'status': case_api,"pass_status":pass_status,"data_list":resp_text})
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取结束时间
    start_time = startTime
    end_time = endTime
    case_total = case_total
    case_pass = str(case_success)
    env_flag = u"根据接口信息配置获取"
    env_num = u"根据接口信息配置获取"
    case_fail = str(case_failed)
    case_mistake = case_mistake
    wc = html_all.replace("{project_cn}", project_cn)
    wc1 = wc.replace("{test_case_detailed}", html_test_msg)
    wc2 = wc1.replace("{start_time}", start_time)
    wc3 = wc2.replace("{end_time}", end_time)
    wc4 = wc3.replace("{case_total}", str(case_total), 2)
    wc5 = wc4.replace("{case_pass}", case_pass, 2)
    wc6 = wc5.replace("{env_flag}", env_flag)
    wc7 = wc6.replace("{env_num}", env_num)
    wc8 = wc7.replace("{case_fail}", case_fail)
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    project_en_sql = "select project_en from project_api where project='%s'"%(project_cn)
    project_en = select_sql(project_en_sql)[0][0]
    path = "./app/base/pythonProject/ReportHtml/{month}/{day}/".format(month=str(month),day=str(day))
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = u"./app/base/pythonProject/ReportHtml/{month}/{day}/{project_en}_schedule.html".format(month=str(month),day=str(day),project_en=project_en)

    with open(file_path,"w") as f:
        f.write(wc8.encode("utf8"))
###发送报告消息
    report_url = u"http://uwsgi.sys.bandubanxie.com/Report/{month}/{day}/{project_en}_schedule.html".format(
        month=str(month), day=str(day), project_en=project_en)
    wechatQY_msg(developer=developer,project_en=project_en,report_url=report_url,
                 success_count=str(case_pass),error_count=str(case_fail),failure_count=str(case_mistake))
    return {'current': current, 'total': case_total, 'status': u'执行成功!','result': case_success,"case_failed":case_failed,"case_mistake":case_mistake}
def run_test(dict_datas,cookies):
    project = dict_datas["project"]  # 业务项目
    url = dict_datas["case_host"] + dict_datas["case_url"] # 请求连接
    method = dict_datas["method"]  # 请求方式
    params = eval(dict_datas["params"])  # 请求参数
    headers = eval(dict_datas["headers"])  # 请求头
    islogin = dict_datas["islogin"]  # 是否需要前置登录
    case_api = dict_datas["case_api"]  # 接口名称
    cookies = eval(cookies)
    if islogin:  # 判断需要登陆状态时，进行登录
        env_flag = cookies["env_flag"]
        env_num = cookies["env_num"]
        account = dict_datas["account"]  #需要登录状态时,获取登录状态
        if account.upper() == "NONE" or account==None:
            account=None
        sql = """select project_en from project_api where project='%s';""" % (project)
        project_en = select_sql(sql)[0][0]  # 获取项目名称
        cookies = get_cookies(project_en,env_flag,env_num,user=account)  # 更新cookies信息，变更为已登录
    try:
        assertValue_dict = None if dict_datas["assertValue"] == "None" or dict_datas["assertValue"] == None else json.loads(dict_datas["assertValue"],
                                                                                       encoding="utf8")  # 校验数据
        if method.upper == "GET":
            resp = getFunction(url=url,headers=headers,params=params,cookies=cookies)
        else:
            resp = postFunction(url=url,headers=headers,params=params,cookies=cookies)
        resp_dict_s = json.loads(resp.text,encoding="utf8")
        status_key_list = []  # 返回key + 验证结果
        status_list = []  # 返回验证结果boolean
        if assertValue_dict==None:
            pass_status = "True"
            return status_key_list,pass_status,resp.text
        else:
            for key in assertValue_dict.keys():
                keyf = None if "None" in key else key
                keyf_value = None if "None" in assertValue_dict[key] else assertValue_dict[key]
                sb = find_key(resp_dict_s, keyf, keyf_value)
                status_key_list.append((key, sb))
                status_list.append(sb)
            if False or None in status_list:
                pass_status = "False"
                return status_key_list,pass_status,resp.text
            else:
                pass_status = "True"
                return status_key_list,pass_status,resp.text
    except Exception as e:
        status_key_list = []
        pass_status = "Mistake"
        error_msg = case_api + ':' + str(e)
        return status_key_list,pass_status,error_msg
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
def wechatQY_msg(developer,project_en,success_count,error_count,failure_count,report_url):
    try:
        content = u"""接口平台调度测试结果:\n测试: {developer} \n测试项目: {project_en} \n通过接口数: {success_count} \n未通过接口数: {error_count} \n程序失败接口数: {failure_count} \n结果查看地址: {report_url}""".format(project_en=project_en,
                                      success_count=success_count,
                                       error_count=error_count,
                                       failure_count=failure_count,
                                       developer=developer,
                                        report_url=report_url
                           )
        params = {
            "tos": u"guohongjie,renhuihui,zhaohongling,pengjunxia,wangmengxiao,hongchen,tianningxue,liushuang,xuhongying,jiayujiao,panze,{developer}".format(
                developer=developer),
            "content": content, "app": "qa", "sed": "guohongjie"}
        qiye_wechat_url = r"http://msg.inf.bandubanxie.com/api/v0.2/msg/qiye_weixin"
        requests.post(url=qiye_wechat_url, data=params)
        return True
    except Exception as e:
        raise Exception,str(e)

if __name__ == "__main__":
    run_api("wctv","云舒写and罐罐熊","GUOHONGJIE")
























