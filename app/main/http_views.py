#-*-coding:utf-8 -*-
from . import test
from flask import request,make_response,jsonify
import requests
from app.base.pythonProject.base.getCookies import *
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
@test.route('/case_http_test',methods = ['POST'])
def case_http_test():
    """
    :param case_host:  domain
    :param case_url:  path
    :param method:  请求方式
    :return:  Response
    """
    project_cn = request.form["project_cn"]
    case_host = request.form["case_host"]
    case_url = request.form["case_url"]
    method = request.form["method"]
    try:
        params = eval(request.form["params"])
        headers = eval(request.form["headers"])
        cookies = eval(request.form["cookies"])
        islogin = request.form["islogin"]
        account = request.form["account"]
        url = case_host + case_url
        if account.upper() == "NONE" or account==None:
            account = None
        if islogin.upper() == "TRUE" or islogin==True:
            if project_cn == "云舒写首页":
                new_cookies = get_wacc_home_cookie(cookies["env_flag"],cookies["env_num"],account).get_dict()
            elif project_cn in ["云舒写后台管理系统","上传文件"]:
                new_cookies = get_wacc_admin_cookie(cookies["env_flag"], cookies["env_num"],account).get_dict()
            elif project_cn == "云舒写CRM系统":
                new_cookies = get_ysx_crm_cookie(cookies["env_flag"], cookies["env_num"],account).get_dict()
            elif project_cn == "简章系统":
                new_cookies = get_wacc_tortoise_cookie(cookies["env_flag"], cookies["env_num"],account).get_dict()
            elif project_cn == "新商品详情系统" or project_cn == "新订单支付系统":
                new_cookies = get_wacc_bird_cookie(cookies["env_flag"], cookies["env_num"],account).get_dict()
            elif project_cn == "云舒写and罐罐熊":
                new_cookies = get_app_cookie(cookies["env_flag"], cookies["env_num"],account).get_dict()
            else:
                raise Exception,"project_cn has not exists or not need set login status!"
        else:
            new_cookies = cookies
        if method=="POST":
            resp = postFunction(url,params,headers,new_cookies)
        elif method=="GET":
            resp = getFunction(url,params,headers,new_cookies)
    except Exception as e:
        resp = str(e)
    response = make_response(jsonify({"code":200,"datas":resp}))  # 返回response
    return response



def postFunction(url,params,headers,cookies):
    resp = requests.post(url,data=params,headers=headers,cookies=cookies)
    return resp.content
def getFunction(url,params,headers,cookies):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies)
    return resp.content