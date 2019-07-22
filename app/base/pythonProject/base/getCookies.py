#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "guohongjie"
import requests
import base64
from PIL import Image
import json
import urllib
import hashlib
import redis
def get_ysx_crm_cookie(env_flag,env_num):
    """登录crm,并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies"""
    url = r"http://admin.crm.yunshuxie.com/captcha.jpg"
    captcha_header = {"Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                      "Accept-Encoding":"gzip, deflate, br",
                      "Cache-Control": "no-cache","Pragma": "no-cache",
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Referer": "https://admin.crm.yunshuxie.com/login.html",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",}
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  #设置测试环境
    cookies.set("env_num",env_num)  #设置环境号
    #cookies.set("ngxUid","8bf5aceda7a0eb92f18e6ba8a3e34613")
    resp = requests.get(url,headers=captcha_header,cookies=cookies)  # 生成验证码
    cookies.update(resp.cookies)  # 更新cookies 容器
    with open("captcha.jpg","wb") as f:  # 存储图片
        f.write(resp.content)
    img = Image.open("captcha.jpg")  # 打开图片
    img = img.crop((44,10,175,45))  # 剪裁图片，提高识别率
    img.save("captcha.jpg")  # 保存图片
    with open("captcha.jpg","rb") as f:  # 打开图片
        base64_img = base64.b64encode(f.read())  # 转换成base64格式图片
        data = {"image_base64":base64_img,
            "app_id":"491861472@NDkxODYxNDcy"}
        url = r"https://nmd-ai.juxinli.com/ocr_captcha"
        captcha_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                              "Content-Type":"application/json"}
        captcha_resp = requests.post(url=url,headers=captcha_header,json=data)  # 获取验证码
        captcha = json.loads(captcha_resp.content,encoding="utf8")["string"].lower()  # 最小化
    url = r"http://admin.crm.yunshuxie.com/sys/login"
    params = {"username": "admin","password": "Yunshuxie916@1ppt","captcha": captcha}  # 登录接口
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

def get_wacc_admin_cookie(env_flag,env_num):
    """ 登录crm, 并返回cookies
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
    params = {"userName": "automation@yunshuxie.com" ,"pwd": "ysx2019"}
    resp = requests.post(url=url, headers=header, cookies=cookies,data=params)
    dict_resp =json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies
def get_wacc_home_cookie(env_flag,env_num):
    """ 登录PC云舒写官网, 并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies
    """
    url = r"https://www.yunshuxie.com/v5/web/account/login.htm"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
              "Accept": "application/json, text/javascript, */*; q=0.01",
              "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9",
              "Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
    params = {"userName": "60000007001" ,"pwd": "123456"}
    resp = requests.post(url=url, headers=header, cookies=cookies,data=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies

def get_wacc_tortoise_cookie(env_flag,env_num):
    """登录销售简章后台配置系统，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    url = r"http://adm.yunshuxie.com/api/sys/login.htm"
    cookies = requests.cookies.RequestsCookieJar() #生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*","Connection":"keep-alive"}
    params = {"userName": "guohongjie", "pwd": "0p80hg56ya"}
    resp = requests.post(url=url, headers=header, cookies=cookies, data=params)
    dict_resp = json.loads(resp.content, encoding="utf8")
    #print dict_resp
    if dict_resp["code"] == "0" or dict_resp["code"] == 0:
        cookies.update(resp.cookies)
    else:
        raise Exception, resp.content
    return cookies

def get_wacc_bird_cookie(env_flag,env_num):
    """登录微信前台开始上课，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    salt = "mengmengda"
    cookies = requests.cookies.RequestsCookieJar() #生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Connection": "keep-alive"
            , "Content-Type": "application/x-www-form-urlencoded",
                  "Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}

    params = {"userName": "60000007001", "pwd": "123456", "type": "3"}
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
def get_app_cookie(env_flag,env_num):
    """登录APP，并返回cookies
    :param env_flag:
    :param env_num:
    :return:
    """
    if env_flag =="beta":
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
    else:
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
    redis_shell = "code_6_60000007001"
    r.set(redis_shell,"123456")
    url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
    salt = "mengmengda"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
    params = {"userName": "60000007001","smsCode": "123456", "type": "10"}
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

def get_cookies(project,env_flag,env_num):
    """
    :param project: 发布项目
    :param env_flag: 发布环境
    :param env_num: 发布环境号
    :return: cookies
    """
    if project == "ysx_crm":
        cookie = get_ysx_crm_cookie(env_flag,env_num).get_dict()
    elif project == "wacc_home":
        cookie = get_wacc_home_cookie(env_flag,env_num).get_dict()
    elif project == "wacc_admin":
        cookie = get_wacc_admin_cookie(env_flag,env_num).get_dict()
    elif project == "wacc_tortoise":
        cookie = get_wacc_tortoise_cookie(env_flag,env_num).get_dict()
    elif project == "wacc_bird":
        cookie = get_wacc_bird_cookie(env_flag,env_num).get_dict()
    elif project == "wacc_mobile":
        cookie = get_app_cookie(env_flag,env_num).get_dict()
    else:
        cookie = {"env_flag":env_flag,"env_num":env_num}

    return cookie

if __name__ == "__main__":
    print get_cookies("wacc_mobile","beta","1")






