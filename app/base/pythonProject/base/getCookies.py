#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "guohongjie"
import requests
import redis
from py_redis import MyRedis
import json
import hashlib
import urllib
import pymysql
def get_ysx_crm_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """登录crm,并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies"""
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  #设置测试环境
    cookies.set("env_num",env_num)  #设置环境号
    username = account_username if account_username else "18519118952"  #默认账号
    password = account_passwd if account_passwd else "123456"  #默认密码
    url = r"https://admin.crm.yunshuxie.com/sys/login"
    params = {"username": username,"password": password,"captcha": "ysx2019"}  # 登录接口
    header = {"Accept": "application/json, text/javascript, */*; q=0.0",
              "Cache-Control": "no-cache",
              "Connection": "keep-alive",
              "Origin": "https://admin.crm.yunshuxie.com",
              "Pragma": "no-cache",
              "Content-Type": "application/x-www-form-urlencoded",
              "Host": "admin.crm.yunshuxie.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    resp = requests.post(url,headers=header,data=params,cookies=cookies)
    cookies.update(resp.cookies)
    result = json.loads(resp.content,encoding="utf8")
    if result["code"] == 0:  # 判断登录是否成功
        return cookies
    else:
        return(get_ysx_crm_cookie(env_flag,env_num))  # 递归
def get_wacc_admin_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """ 登录admin, 并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies
    """
    url = r"https://admin.yunshuxie.com/common_index/loginIn.json"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Accept": "application/json, text/javascript, */*; q=0.01",
              "Accept-Encoding": "gzip, deflate, br",
              "Accept-Language": "zh-CN,zh;q=0.9",
              "Cache-Control": "no-cache","Connection": "keep-alive",
              "Content-Length": "73",
              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Origin": "https://admin.yunshuxie.com",
              "Pragma": "no-cache","Referer": "https://admin.yunshuxie.com/","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    username = account_username if account_username else "automation@yunshuxie.com"  #默认账号
    pwd = account_passwd if account_passwd else "ysx2019"  #默认密码
    params = {"userName": username ,"pwd": pwd,"emailVerifyCode":"ysx2019"}
    resp = requests.post(url=url, headers=header, cookies=cookies,data=params)
    dict_resp =json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_home_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """ 登录PC云舒写官网, 并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies
    """
    r = MyRedis()
    user = account_username if account_username else r.str_get("wacc_home_user_phone")
    url = r"https://www.yunshuxie.com/v5/web/account/login.htm"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
              "Accept": "application/json, text/javascript, */*; q=0.01",
              "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9",
              "Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
    username = user if user else "60000007001"  #默认账号
    pwd = account_passwd if account_passwd else "test123456"  #默认密码
    params = {"userName": username ,"pwd": pwd }
    resp = requests.post(url=url, headers=header, cookies=cookies,data=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_tortoise_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """登录销售简章后台配置系统，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    r = MyRedis()
    username = r.str_get("wacc_tortoise_user")
    url = r"http://adm.yunshuxie.com/api/sys/login.htm"
    cookies = requests.cookies.RequestsCookieJar() #生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*","Connection":"keep-alive"}
    username = account_username if account_username else "guohongjie"  # 默认账号
    pwd = account_passwd if account_passwd else "0p80hg56ya"  # 默认密码
    params = {"userName": username, "pwd": pwd}
    resp = requests.post(url=url, headers=header, cookies=cookies, data=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["code"] == "0" or dict_resp["code"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_bird_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """登录微信前台开始上课，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    r = MyRedis()
    user = account_username if account_username else r.str_get("wacc_bird_user_phone")
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    salt = "mengmengda"
    cookies = requests.cookies.RequestsCookieJar() #生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Connection": "keep-alive"
            , "Content-Type": "application/x-www-form-urlencoded",
                  "Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}

    username = user if user else "60000007001"  # 默认账号
    pwd = account_passwd if account_passwd else "test123456"  # 默认密码
    params = {"userName": username, "pwd": pwd, "type": "3"}
    string = urllib.urlencode(params)
    s = string + salt
    md = hashlib.md5()
    md.update(s)
    md5 = md.hexdigest()
    data = string + "&sign=" + md5
    resp = requests.post(url=url, headers=header, cookies=cookies, data=data)
    dict_resp = json.loads(resp.content, encoding="utf8")
    if dict_resp["code"] == "0" or dict_resp["code"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_app_cookie(project_cn,env_flag,env_num,account_username=None,account_passwd=None):
    """登录移动端APP，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    w = MyRedis()
    user = account_username if account_username else w.str_get("wacc_mobile_user_phone")
    if env_flag =="beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
    if project_cn == "罐罐熊APP":
        redis_shell = "code_6_" + user
    elif project_cn == "云舒写APP":
        redis_shell = "code_2_" + user
    else:
        redis_shell = "code_6_" + user
    r.set(redis_shell,"123456")
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    salt = "mengmengda"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
    username = user if user else "60000007001"  # 默认账号
    pwd = account_passwd if account_passwd else "123456"  # 默认密码
    params = {"userName": username,"smsCode": pwd, "type": "10"}
    string = urllib.urlencode(params)
    s = string + salt
    md = hashlib.md5()
    md.update(s)
    md5 = md.hexdigest()
    data = string + "&sign=" + md5
    resp = requests.post(url=url, headers=header, cookies=cookies, data=data)
    dict_resp = json.loads(resp.content, encoding="utf8")
    if dict_resp["code"] == "0" or dict_resp["code"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wechat_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """微信公众号登录"""
    session = requests.Session()
    request_retry = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("https://", request_retry)
    session.mount("http://", request_retry)
    cookies = requests.cookies.RequestsCookieJar()
    header = {"Connection": "keep-alive"
        , "Content-Type": "application/x-www-form-urlencoded",
              "Cache-Control": "no-cache",
              "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}

    session.headers = header
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    session.cookies = cookies
    salt = "mengmengda"
    if env_flag=="beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
        r.set("SESS:LOGIN:WXTEMPCODE_081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc",
              "{\"openid\":\"o38sIv0DUSADJyxT2Ebd-MN4lFXE\",\"nickname\":\"自动化测试\",\"sex\":1,\"language\":\"zh_CN\",\"city\":\"Haidian\",\"province\":\"Beijing\",\"country\":\"CN\",\"headimgurl\":\"http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLfOZiaOCKuckMxTnicDO79Aibn5SVWQRiaSOQuyMJKiaxUCgZrh4JlWOOibHo03Yu8PkkmYs1zgwJedGvQ/132\",\"privilege\":[],\"unionid\":\"o_Pn8sxP5oST2gCYgl-kcGSeILBo\"}")
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
        r.set("SESS:LOGIN:WXTEMPCODE_081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc",
              "{\"openid\":\"o38sIv0DUSADJyxT2Ebd-MN4lFXE\",\"nickname\":\"自动化测试\",\"sex\":1,\"language\":\"zh_CN\",\"city\":\"Haidian\",\"province\":\"Beijing\",\"country\":\"CN\",\"headimgurl\":\"http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLfOZiaOCKuckMxTnicDO79Aibn5SVWQRiaSOQuyMJKiaxUCgZrh4JlWOOibHo03Yu8PkkmYs1zgwJedGvQ/132\",\"privilege\":[],\"unionid\":\"o_Pn8sxP5oST2gCYgl-kcGSeILBo\"}")

    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    username = account_username if account_username else "60000007001"  # 默认账号
    pwd = account_passwd if account_passwd else "test123456"  # 默认密码
    params = {"userName": username, "pwd": pwd, "type": "2","wechatCode":"081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc"}
    string = urllib.urlencode(params)
    s = string + salt
    md = hashlib.md5()
    md.update(s)
    md5 = md.hexdigest()
    data = string + "&sign=" + md5
    resp = session.post(url, data=data)
    print resp.content
    dict_resp = json.loads(resp.content, encoding="utf8")
    if dict_resp["code"] == "0" or dict_resp["code"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wechat_capth_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """微信公众号验证码登录"""
    salt = "mengmengda"
    session = requests.Session()
    request_retry = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("https://", request_retry)
    session.mount("http://", request_retry)
    header = {"Connection": "keep-alive"
        , "Content-Type": "application/x-www-form-urlencoded",
              "Cache-Control": "no-cache",
              "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
    session.headers = header
    cookies = {"env_flag": env_flag, "env_num": env_num}
    session.cookies = requests.utils.cookiejar_from_dict(cookies)
    params_get_phone_code = {"phone": account_username, "verType": "2"}  # 1登录 ;2修改手机号
    if env_flag=="beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
        r.set("SESS:LOGIN:WXTEMPCODE_081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc",
              "{\"openid\":\"o38sIv0DUSADJyxT2Ebd-MN4lFXE\",\"nickname\":\"自动化测试\",\"sex\":1,\"language\":\"zh_CN\",\"city\":\"Haidian\",\"province\":\"Beijing\",\"country\":\"CN\",\"headimgurl\":\"http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLfOZiaOCKuckMxTnicDO79Aibn5SVWQRiaSOQuyMJKiaxUCgZrh4JlWOOibHo03Yu8PkkmYs1zgwJedGvQ/132\",\"privilege\":[],\"unionid\":\"o_Pn8sxP5oST2gCYgl-kcGSeILBo\"}")
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
        r.set("SESS:LOGIN:WXTEMPCODE_081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc",
              "{\"openid\":\"o38sIv0DUSADJyxT2Ebd-MN4lFXE\",\"nickname\":\"自动化测试\",\"sex\":1,\"language\":\"zh_CN\",\"city\":\"Haidian\",\"province\":\"Beijing\",\"country\":\"CN\",\"headimgurl\":\"http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLfOZiaOCKuckMxTnicDO79Aibn5SVWQRiaSOQuyMJKiaxUCgZrh4JlWOOibHo03Yu8PkkmYs1zgwJedGvQ/132\",\"privilege\":[],\"unionid\":\"o_Pn8sxP5oST2gCYgl-kcGSeILBo\"}")
    redis_shell = "code_" + params_get_phone_code["verType"] + "_" + params_get_phone_code["phone"]
    r.set(redis_shell,"123456")
    capth = r.get(redis_shell)
    expect = {"code": "0"}
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    # PC登录
    username = account_username if account_username else "60000007001"  # 默认账号
    capth = capth if capth else "123456"  # 默认密码
    params = {"userName": username, "smsCode": capth, "type": "9","wechatCode":"081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc"}
    string = urllib.urlencode(params)
    s = string + salt
    md = hashlib.md5()
    md.update(s)
    md5 = md.hexdigest()
    data = string + "&sign=" + md5
    resp = session.post(url, data=data)  # PC短信验证码登录
    print resp.content
    cookies = resp.cookies
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    return cookies
def get_wechat_ggx_cookies(env_flag,env_num,account_username=None,account_passwd=None):
    """微信罐罐熊小程序登录"""
    session = requests.Session()
    request_retry = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("https://", request_retry)
    session.mount("http://", request_retry)
    cookies = requests.cookies.RequestsCookieJar()
    header = {"Connection": "keep-alive"
        , "Content-Type": "application/x-www-form-urlencoded",
              "Cache-Control": "no-cache",
              "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
    session.headers = header
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    cookies.set("name","mp-bear")
    session.cookies = cookies
    if env_flag=="beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
    r.set("code_6_%s"%(account_username),"1234561","60")
    url = r"http://wap.yunshuxie.com/v1/mini/login.htm"
    username = account_username if account_username else "60000007001"  # 默认账号
    passwd = account_passwd if account_passwd else "1234561"  # 默认密码
    params = {"phone":username,"validate":passwd,"userType":"67","openId":"oPPdW4-Ty_9hIDlEGgRto5NLIGo4","unionId":"o_Pn8s8QLZF4OEgQsxJTNqSkDAbI","isApp":"1"}
    resp = session.get(url, params=params)
    print resp.content
    dict_resp = json.loads(resp.content, encoding="utf8")
    cookies.set("SessionKey",dict_resp['data']['token'])
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wechat_teaco_cookies(env_flag,env_num,account_username=None,account_passwd=None):
    """微信小程序教师端登录"""
    cookies = requests.cookies.RequestsCookieJar()
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    if env_flag=="beta":
        db = pymysql.connect("172.17.1.239", "ysx_beta_writer", "rzcXYilPKauGMCIz1dQ3AOzzO7Y-", "ysx_teaching_community", port=3317, charset='utf8')
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
    else:
        db = pymysql.connect("172.17.1.42", "ysx_prod_writer", "RIdqXTBJyQmK8yBqmytnE69OOM1-", "ysx_teaching_community", port=3307, charset='utf8')
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
    if account_username:
        cursor = db.cursor()
        cursor.execute("select id from ysx_user where wechat_nick='{wechat_nick}'".format(wechat_nick=account_username))
        data = cursor.fetchall()
        db.close()
        userId = data[0][0]
        r.set("user_session_key:%s"%("wctv"), userId,60)
        cookies.set("SessionKey", "wctv")  # 设置环境号
    else:
        cookies = cookies
    return cookies
def get_adm_single_cookies(env_flag,env_num,account_username=None,account_passwd=None):
    """单点登录系统&admin"""
    session = requests.Session()
    request_retry = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("https://", request_retry)
    session.mount("http://", request_retry)
    cookies = requests.cookies.RequestsCookieJar()
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    domain = "https://sso.yunshuxie.com"
    url = "/auth/verifyCode"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"}
    session.headers = headers
    session.cookies = cookies
    resp = session.get(url=domain + url)
    dict_resp = json.loads(resp.text, encoding="utf-8")
    tokenId = dict_resp["data"]["tokenId"]
    if env_flag == "beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password",db=1)
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password",db=1)
    captch = r.get(tokenId)
    login_url = "/auth/login"
    pwd = account_passwd if account_passwd else "123456"
    hl = hashlib.md5()
    hl.update(pwd)
    md5_pwd = hl.hexdigest()
    username = account_username if account_username else "60000007001"  # 默认账号
    params = {"username":username,
              "password":md5_pwd,
              "verifyCode":captch,"tokenId":tokenId,"sso_app_id":"adm"}
    resp = session.post(url=domain+login_url,data=params)
    dict_resp = json.loads(resp.text,encoding="utf-8")
    cookies.set("sso_sessionid", dict_resp["data"]["sessionId"])
    cookies.update(resp.cookies)
    return cookies
def get_material_platform_cookies(env_flag,env_num,account_username=None,account_passwd=None):
    """物料平台登录"""
    url = r"https://pay.yunshuxie.com/v5/sales_poster/sale_loginV2.htm"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    username = account_username if account_username else "60000007001"
    pwd = account_passwd if account_passwd else "test123.."
    params = {"phone": username,"pwd": pwd}
    resp = requests.get(url=url, headers=header, cookies=cookies, params=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    # print dict_resp
    print dict_resp["data"]["shareKey"]
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies


def get_cookies(project,env_flag,env_num,account_username=None,account_passwd=None):
    """
    :param project: 发布项目
    :param env_flag: 发布环境
    :param env_num: 发布环境号
    :return: cookies
    """
    if project == "云舒写CRM系统":
        cookie = get_ysx_crm_cookie(env_flag,env_num,account_username,account_passwd).get_dict()
    elif project == "云舒写官网首页":
        cookie = get_wacc_home_cookie(env_flag,env_num,account_username,account_passwd).get_dict()
    elif project == "云舒写ADMIN后台管理系统":
        cookie = get_wacc_admin_cookie(env_flag,env_num,account_username,account_passwd).get_dict()
    elif project == "简章系统":
        cookie = get_wacc_tortoise_cookie(env_flag,env_num,account_username,account_passwd).get_dict()
    elif project == "新商品详情系统" or project == "新订单支付系统":
        cookie = get_wacc_bird_cookie(env_flag,env_num,account_username,account_passwd).get_dict()
    elif project in ["罐罐熊APP","云舒写APP"]:
        cookie = get_app_cookie(project,env_flag,env_num,account_username,account_passwd).get_dict()
    elif project == "罐罐熊练字课微信小程序":
        cookie = get_wechat_ggx_cookies(env_flag,env_num,account_username,account_passwd)
    elif project == "云舒写大语文合作与推广":
        cookie = get_wechat_capth_cookie(env_flag,env_num,account_username,account_passwd)
    elif project == "陪你阅读陪你写作":
        cookie = get_wechat_cookie(env_flag,env_num, account_username,account_passwd)
    elif project == "教师端资料库小程序":
        cookie = get_wechat_teaco_cookies(env_flag,env_num,account_username,account_passwd)
    elif project == "单点登录系统admin平台":
        cookie = get_adm_single_cookies(env_flag,env_num,account_username,account_passwd)
    elif project == "物料领取平台":
        cookie = get_material_platform_cookies(env_flag,env_num,account_username,account_passwd)
    elif project == "短信服务":
        cookie = {"env_flag": env_flag, "env_num": env_num}
    elif project == "用户行为":
        cookie = {"env_flag": env_flag, "env_num": env_num}
    else:
        cookie = {"env_flag":env_flag,"env_num":env_num}

    return cookie

if __name__ == "__main__":
    #print get_wechat_teaco_cookies("beta","5","向前！向前！")
    phone = 60000012616
    #while True:
#
    get_material_platform_cookies("beta","8","%s"%(phone))
      #  phone += 1
     #   if phone>60000012530:
       #     break

