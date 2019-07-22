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
        url = case_host + case_url
        if project_cn == "云舒写首页":
            cookies = get_wacc_home_cookie(cookies["env_flag"],cookies["env_num"]).get_dict()
        if project_cn in ["云舒写后台管理系统","上传文件"]:
            cookies = get_wacc_admin_cookie(cookies["env_flag"], cookies["env_num"]).get_dict()
        if project_cn == "云舒写CRM系统":
            cookies = get_ysx_crm_cookie(cookies["env_flag"], cookies["env_num"]).get_dict()
        if project_cn == "简章系统":
            cookies = get_wacc_tortoise_cookie(cookies["env_flag"], cookies["env_num"]).get_dict()
        if project_cn == "新商品详情系统" or project_cn == "新订单支付系统":
            cookies = get_wacc_bird_cookie(cookies["env_flag"], cookies["env_num"]).get_dict()
        if project_cn == "云舒写&罐罐熊(APP)":
            cookies = get_app_cookie(cookies["env_flag"], cookies["env_num"]).get_dict()
        if method=="POST":
            resp = postFunction(url,params,headers,cookies)
        elif method=="GET":
            resp = getFunction(url,params,headers,cookies)
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