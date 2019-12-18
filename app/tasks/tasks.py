#!/usr/bin/python
#-*-coding:utf-8 -*-
from celery_app import celery,MyTask
from app.config.sql import select_sql
from app.config.html_template import test_case_detailed,html_all
from app.base.pythonProject.base.getCookies import get_cookies
from app.base.pythonProject.run import run_yunwei_case
from app.config.project_loginIn import replace_cn
import requests
import datetime
import json
import os
import re
#持续集成调度测试

@celery.task(bind=True,base=MyTask)
def run_schedule_api(self,origin=None,originParams=None,cookies=None,developer=None):
    if origin=="doSelfSchedule":    #手工调度发起
        keys = ["project", "case_api", "case_host", "case_url", "method", "params", "headers","description",
                "islogin", "account_project","account_username","account_passwd","isSchedule","checkAssert"]
        datas_list = []
        for key,api_datas in originParams.items():
            api_dict_datas = json.loads(api_datas)
            project,case_api,api_pid = api_dict_datas["project"],api_dict_datas["case_api"],api_dict_datas["api_pid"]
            sql = """
            select 
                project,case_api,case_host,case_url,method,params,headers,description,
                islogin,account_project,account_username,account_passwd,isSchedule,checkAssert
            from
                case_http_api 
            where
                project='%s' and case_api='%s' and id='%s'
            """%(project,case_api,api_pid)
            datas = select_sql(sql)
            for data in datas:
                key_value = dict(zip(keys, data))
                datas_list.append(key_value)
    else:    #持续集成调度发起
        project = originParams
        sql = """
        select 
            cha.project,cha.case_api,cha.case_host,cha.case_url,cha.method,
            chs.params,chs.assertValue,
            cha.headers,cha.islogin,
            cha.account_project,cha.account_username,cha.account_passwd
        from 
            case_http_api cha, case_http_schedule chs 
        where
            cha.id = chs.api_id and cha.project='%s' 
            and chs.status=1 """%(project)
        datas = select_sql(sql)
        datas_list = []
        keys = ["project", "case_api", "case_host", "case_url", "method", "params","assertValue",
                "headers","islogin", "account_project", "account_username", "account_passwd"]
        for data in datas:
            key_value = dict(zip(keys,data))
            datas_list.append(key_value)

    html_test_msg = ""
    case_total = len(datas_list)   #全部用例
    current = 0  #计数器
    case_success = 0  #成功用例数
    case_mistake = 0  #代码错误用例数
    case_failed = 0  #失败用例数
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取开始时间
    for i in range(case_total):
        current += 1  # 计数器+1
        case_api = datas_list[i]["case_api"]  # 接口名称
        case_url = datas_list[i]["case_host"] + datas_list[i]["case_url"]
        case_params = datas_list[i]["params"]
        if origin == "doSelfSchedule":
            resp_status,resp_text = run_test(origin,datas_list[i],cookies)  # 手工调度传入 单条 接口用例数据
        else:
            resp_status, resp_text = run_test(origin,datas_list[i], cookies)  # 集成调度传入 单条 接口用例数据
        if resp_status =="Success":
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
        responce_params = resp_text  #"返回参数"
        method = datas_list[i]["method"]
        project_cn = datas_list[i]["project"]
        description = datas_list[i]["description"]
        if pass_status == 1:
            status_color = "btn-success"
            case_status = u"通过"
        elif pass_status==0:
            status_color = "btn-danger"
            case_status = u"失败"
        else:
            status_color = "btn-danger"
            case_status = u"返回错误"
        new_detailed = test_case_detailed.format(api_name=api_name, method=method, api_url=api_url,description=description,
                                                 request_params=request_params,
                                                 status_color=status_color, case_status=case_status,
                                                 responce_params=responce_params,pid=str(i))
        html_test_msg += new_detailed
        # self.update_state(state='PROGRESS',
        #                   meta={'current': i, 'total': case_total,
        #                        'status': case_api,"pass_status":pass_status,"data_list":resp_text})
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取结束时间
    start_time = startTime
    end_time = endTime
    case_total = case_total
    case_pass = str(case_success)
    env_flag = cookies["env_flag"]
    env_num = cookies["env_num"]
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
    file_path = u"./app/base/pythonProject/ReportHtml/{month}/{day}/{project_cn}_schedule.html".format(month=str(month),day=str(day),project_cn=project_cn)

    with open(file_path,"w") as f:
        f.write(wc8.encode("utf8"))
###发送报告消息
    report_url = u"http://uwsgi.sys.bandubanxie.com/Report/{month}/{day}/{project_en}_schedule.html".format(
        month=str(month), day=str(day), project_en=project_cn)
    wechatQY_msg(developer=developer,project_cn=project_cn,report_url=report_url,
                 success_count=str(case_pass),fail_count=str(case_fail),mistake_count=str(case_mistake))
    return {'current': current, 'total': case_total, 'status': u'执行成功!','result': case_success,"case_failed":case_failed,"case_mistake":case_mistake}

#持续集成业务流程调度测试
@celery.task()
def run_api_case(project_en,env_num,env_flag,description,project_cn,new_phone=None,developer=None,developer_project=None,branch=None):
    try:#project_en,env_num,env_flag,description,project_cn,new_phone=None,developer=None,developer_project=None,branch=None
        run_yunwei_case(project_en=project_en,
                        env_num=env_num,
                        env_flag=env_flag,description=description,
                        project_cn=project_cn,new_phone=new_phone,developer=developer,developer_project=developer_project,branch=branch)
        return u"执行成功!"
    except Exception as e:
        return str(e)

def run_test(origin,dict_datas,cookies):
    try:
        if origin == "doSelfSchedule":
            url = dict_datas["case_host"] + dict_datas["case_url"]  # 请求连接
            method = dict_datas["method"]  # 请求方式
            headers = eval(replace_cn(dict_datas["headers"].strip()))  # 请求头
            islogin = dict_datas["islogin"]  # 是否需要前置登录
            case_api = dict_datas["case_api"]  # 接口名称
            isSchedule = dict_datas["isSchedule"]
            checkAssert = dict_datas["checkAssert"]
            cookies = cookies
            params = eval(replace_cn(dict_datas["params"].strip()))  # 请求参数
        else:    #集成调度
            project = dict_datas["project"]  # 业务项目
            url = dict_datas["case_host"] + dict_datas["case_url"]  # 请求连接
            method = dict_datas["method"]  # 请求方式
            assertValue = dict_datas["assertValue"]
            headers = eval(replace_cn(dict_datas["headers"]).strip())  # 请求头
            islogin = dict_datas["islogin"]  # 是否需要前置登录
            case_api = dict_datas["case_api"]  # 接口名称
            cookies = cookies
            params = eval(replace_cn(dict_datas["params"].strip()))  # 请求参数(需要进行参数传递设置,暂时不修改)
    except Exception as e:
        pass_status = "Mistake"
        error_msg = "参数错误,请检查参数"
        return pass_status, error_msg
    else:
        try:
            if islogin:  # 判断需要登陆状态时，进行登录
                env_flag = cookies["env_flag"]
                env_num = cookies["env_num"]
                account_project = dict_datas["account_project"]  #需要登录状态时,获取登录状态
                account_username = dict_datas["account_username"]
                account_password = dict_datas["account_passwd"]
                if not account_username and not account_project or not account_password:
                    account_project, account_username, account_password = None, None, None
                elif account_project.upper() == "NONE" and account_username.upper() == "NONE" or account_password.upper() == "NONE":
                    account_project,account_username,account_password = None,None,None
                cookies = get_cookies(account_project,env_flag,env_num,
                                      account_username=account_username,
                                      account_passwd=account_password)  # 更新cookies信息，变更为已登录
                if cookies["code"] != 200:
                    raise Exception,"登录失败!请检查用户名密码!"
                else:
                    new_cookies = cookies["cookies"].get_dict()
                    if method.upper() == "GET":
                        resp = getFunction(url=url, headers=headers, params=params, cookies=new_cookies)
                    else:
                        resp = postFunction(url=url, headers=headers, params=params, cookies=new_cookies)
            else:
                cookies = cookies
                if method.upper() == "GET":
                    resp = getFunction(url=url,headers=headers,params=params,cookies=cookies)
                else:
                    resp = postFunction(url=url,headers=headers,params=params,cookies=cookies)
            if origin == "doSelfSchedule":    #判断当前调度等于手工调度
                if resp.status_code == 200:
                    if isSchedule:    #参加校验
                        assert_list = checkAssert.split(",")
                        for assert_value in assert_list:
                            assertResult = re.findall(assert_value,resp.text)
                            if assertResult:
                                pass_status = "Success"
                            else:
                                pass_status = "Failure"
                    else:    #不参加校验
                        pass_status = "Success"
                else:
                    pass_status = "Failure"
            else:    #集成调度(需要进行参数值校验,暂时不添加)
                if resp.status_code == 200:
                    try:
                        resp_dict = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                        pass_status = "Success"
                    except Exception as e:
                        pass_status = "Failure"
                else:
                    pass_status = "Mistake"
            return pass_status,resp.text
        except Exception as e:
            pass_status = "Mistake"
            error_msg = case_api + ':' + str(e)
            return pass_status,error_msg
def postFunction(url, params, headers, cookies):
    resp = requests.post(url, data=params, headers=headers, cookies=cookies)
    return resp
def getFunction(url, params, headers, cookies):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies)
    return resp
def wechatQY_msg(developer,project_cn,success_count,fail_count,mistake_count,report_url):
    try:
        content = u"""接口平台调度测试结果:\n测试: {developer} \n测试项目: {project_en} \n通过接口数: {success_count} \n未通过接口数: {fail_count} \n程序失败接口数: {mistake_count} \n结果查看地址: {report_url}""".format(project_en=project_cn,
                                      success_count=success_count,
                                       fail_count=fail_count,
                                       mistake_count=mistake_count,
                                       developer=developer,
                                        report_url=report_url
                           )
        params = {
            "tos": u"guohongjie,renhuihui,zhaohongling,pengjunxia,wangmengxiao,hongchen,tianningxue,liushuang,xuhongying,jiayujiao,panze,huyanfeng,liangguoqing,{developer}".format(
                developer=developer),
            "content": content, "app": "qa", "sed": "guohongjie"}
        qiye_wechat_url = r"http://msg.inf.bandubanxie.com/api/v0.2/msg/qiye_weixin"
        requests.post(url=qiye_wechat_url, data=params)
        return True
    except Exception as e:
        raise Exception,str(e)

if __name__ == "__main__":
    run_schedule_api("",origin="doSelfSchedule",originParams=None,cookies=None,developer=None)
























