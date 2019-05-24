#-*-coding:utf-8 -*-
from . import test
from flask import request,make_response,jsonify
import requests
import json
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
    case_host = request.form["case_host"]
    case_url = request.form["case_url"]
    method = request.form["method"]
    try:
        params = eval(request.form["params"])
        headers = eval(request.form["headers"])
        cookies = eval(request.form["cookies"])
        url = case_host + case_url
        # if cookies == "None":
        #     cookies = None
        # if headers == "None":
        #     headers = None
        # if params == "None":
        #     params = None
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