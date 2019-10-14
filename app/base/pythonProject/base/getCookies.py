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
def get_ysx_crm_cookie(env_flag,env_num,user=None):
    """登录crm,并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies"""
    #url = r"http://admin.crm.yunshuxie.com/captcha.jpg"
    #captcha_header = {"Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    #                  "Accept-Encoding":"gzip, deflate, br",
    #                  "Cache-Control": "no-cache","Pragma": "no-cache",
    #                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #                  "Referer": "https://admin.crm.yunshuxie.com/login.html",
    #                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",}
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  #设置测试环境
    cookies.set("env_num",env_num)  #设置环境号
    #cookies.set("ngxUid","8bf5aceda7a0eb92f18e6ba8a3e34613")
    #resp = requests.get(url,headers=captcha_header,cookies=cookies)  # 生成验证码
    #cookies.update(resp.cookies)  # 更新cookies 容器
    #with open("captcha.jpg","wb") as f:  # 存储图片
    #    f.write(resp.content)
    #img = Image.open("captcha.jpg")  # 打开图片
    #img = img.crop((44,10,175,45))  # 剪裁图片，提高识别率
    #img.save("captcha.jpg")  # 保存图片
    #with open("captcha.jpg","rb") as f:  # 打开图片
    #    base64_img = base64.b64encode(f.read())  # 转换成base64格式图片
    #    data = {"image_base64":base64_img,
    #        "app_id":"491861472@NDkxODYxNDcy"}
    #    url = r"https://nmd-ai.juxinli.com/ocr_captcha"
    #    captcha_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    #                          "Content-Type":"application/json"}
    #    captcha_resp = requests.post(url=url,headers=captcha_header,json=data)  # 获取验证码
    #    captcha = json.loads(captcha_resp.content,encoding="utf8")["string"].lower()  # 最小化
    url = r"https://admin.crm.yunshuxie.com/sys/login"
    params = {"username": "18519118952","password": "123456","captcha": "ysx2019"}  # 登录接口
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
def get_wacc_admin_cookie(env_flag,env_num,user=None):
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
    params = {"userName": "automation@yunshuxie.com" ,"pwd": "ysx2019","emailVerifyCode":"ysx2019"}
    resp = requests.post(url=url, headers=header, cookies=cookies,data=params)
    dict_resp =json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_home_cookie(env_flag,env_num,user=None):
    """ 登录PC云舒写官网, 并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies
    """
    r = MyRedis()
    user = user if user else r.str_get("wacc_home_user_phone")
    url = r"https://www.yunshuxie.com/v5/web/account/login.htm"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
              "Accept": "application/json, text/javascript, */*; q=0.01",
              "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9",
              "Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
    params = {"userName": user ,"pwd": "123456"}
    resp = requests.post(url=url, headers=header, cookies=cookies,data=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_tortoise_cookie(env_flag,env_num,user=None):
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
    params = {"userName": username, "pwd": "0p80hg56ya"}
    resp = requests.post(url=url, headers=header, cookies=cookies, data=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["code"] == "0" or dict_resp["code"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_bird_cookie(env_flag,env_num,user=None):
    """登录微信前台开始上课，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    r = MyRedis()
    user = user if user else r.str_get("wacc_bird_user_phone")
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    salt = "mengmengda"
    cookies = requests.cookies.RequestsCookieJar() #生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Connection": "keep-alive"
            , "Content-Type": "application/x-www-form-urlencoded",
                  "Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}

    params = {"userName": user, "pwd": "123456", "type": "3"}
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
def get_app_cookie(env_flag,env_num,user=None):
    """登录移动端APP，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    w = MyRedis()
    user = user if user else w.str_get("wacc_mobile_user_phone")
    if env_flag =="beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
    redis_shell = "code_6_" + user
    r.set(redis_shell,"123456")
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    salt = "mengmengda"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
    params = {"userName": user,"smsCode": "123456", "type": "10"}
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
def get_wechat_cookie(env_flag,env_num,user=None):
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
    params = {"userName": user, "pwd": "test123456", "type": "2","wechatCode":"081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc"}
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
def get_wechat_capth_cookie(env_flag,env_num,user=None):
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
    #url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
    params_get_phone_code = {"phone": user, "verType": "2"}  # 1登录 ;2修改手机号
    #string = urllib.urlencode(params_get_phone_code)
    #s = string + salt
    #md = hashlib.md5()
    #md.update(s)
    #md5 = md.hexdigest()
    #data = string + "&sign=" + md5
    #resp = session.post(url, data=data)
    #dict_resp = json.loads(resp.content, encoding="utf8")
    # print self.resp.content
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
    params = {"userName": user, "smsCode": capth, "type": "9","wechatCode":"081S9XOa0bkKqx1PRyOa0pPMOa0S9XOc"}
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
def get_wechat_ggx_cookies(env_flag,env_num,user=None):
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
    r.set("code_6_%s"%(user),"1234561","60")
    url = r"http://wap.yunshuxie.com/v1/mini/login.htm"
    params = {"phone":user,"validate":"1234561","userType":"67","openId":"oPPdW4-Ty_9hIDlEGgRto5NLIGo4","unionId":"o_Pn8s8QLZF4OEgQsxJTNqSkDAbI","isApp":"1"}
    resp = session.get(url, params=params)
    print resp.content
    dict_resp = json.loads(resp.content, encoding="utf8")
    cookies.set("SessionKey",dict_resp['data']['token'])
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wechat_teaco_cookies(env_flag,env_num,user=None):
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
    if user:
        cursor = db.cursor()
        cursor.execute("select id from ysx_user where wechat_nick='{wechat_nick}'".format(wechat_nick=user))
        data = cursor.fetchall()
        db.close()
        userId = data[0][0]
        r.set("user_session_key:%s"%("wctv"), userId,60)
        cookies.set("SessionKey", "wctv")  # 设置环境号
    else:
        cookies = cookies
    return cookies
def get_adm_single_cookies(env_flag,env_num,user=None):
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
    pwd = "123456"
    hl = hashlib.md5()
    hl.update(pwd)
    md5_pwd = hl.hexdigest()
    params = {"username":user,
              "password":md5_pwd,
              "verifyCode":captch,"tokenId":tokenId,"sso_app_id":"adm"}
    resp = session.post(url=domain+login_url,data=params)
    dict_resp = json.loads(resp.text,encoding="utf-8")
    cookies.set("sso_sessionid", dict_resp["data"]["sessionId"])
    cookies.update(resp.cookies)
    return cookies

def get_cookies(project,env_flag,env_num,user=None):
    """
    :param project: 发布项目
    :param env_flag: 发布环境
    :param env_num: 发布环境号
    :return: cookies
    """
    if project == "云舒写CRM系统":
        cookie = get_ysx_crm_cookie(env_flag,env_num,user).get_dict()
    elif project == "云舒写首页":
        cookie = get_wacc_home_cookie(env_flag,env_num,user).get_dict()
    elif project == "云舒写后台管理系统":
        cookie = get_wacc_admin_cookie(env_flag,env_num,user).get_dict()
    elif project == "简章系统":
        cookie = get_wacc_tortoise_cookie(env_flag,env_num,user).get_dict()
    elif project == "新商品详情系统" or project == "新订单支付系统":
        cookie = get_wacc_bird_cookie(env_flag,env_num,user).get_dict()
    elif project == "罐罐熊APP":
        cookie = get_app_cookie(env_flag,env_num,user).get_dict()
    elif project == "罐罐熊练字课微信小程序":
        cookie = get_wechat_ggx_cookies(env_flag,env_num,user)
    elif project == "云舒写大语文合作与推广":
        cookie = get_wechat_capth_cookie(env_flag,env_num,user)
    elif project == "陪你阅读陪你写作":
        cookie = get_wechat_cookie(env_flag,env_num, user)
    elif project == "教师端资料库小程序":
        cookie = get_wechat_teaco_cookies(env_flag,env_num,user)
    elif project == "单点登录系统admin平台":
        cookie = get_adm_single_cookies(env_flag,env_num,user)
    elif project == "短信服务":
        cookie = {"env_flag": env_flag, "env_num": env_num}
    elif project == "用户行为":
        cookie = {"env_flag": env_flag, "env_num": env_num}
    else:
        cookie = {"env_flag":env_flag,"env_num":env_num}
    return cookie

if __name__ == "__main__":
    #print get_wechat_teaco_cookies("beta","5","向前！向前！")
    print get_cookies("单点登录系统admin平台","beta","1","rocky").get_dict()


