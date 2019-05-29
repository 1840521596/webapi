#!/usr/bin/python
#-*-coding:utf-8 -*-

# import requests
# import hashlib
# import urllib
# session = requests.Session()
# request_retry = requests.adapters.HTTPAdapter(max_retries=3)
# session.mount("https://",request_retry)
# session.mount("http://",request_retry)
# header = {"Connection":"keep-alive"
#         ,"Content-Type": "application/x-www-form-urlencoded",
#           "Cache-Control":"no-cache",
#           "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
#
# session.headers = header
# cookies = {"env_flag":"beta","env_num":"2"}
# session.cookies = requests.utils.cookiejar_from_dict(cookies)
# salt= "mengmengda"
# # 账号密码登录
# url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
# params = {"userName":"60000007001","pwd":"123456","type":"1"}
# string = urllib.urlencode(params)
# s = string+salt
# md = hashlib.md5()
# md.update(s)
# md5 = md.hexdigest()
# data = string+"&sign="+md5
# print data
# resp = session.post(url,data=data)
# print resp.content

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth : pangguoping

import pika

pwd = "pwd"
def wc():
    print "wc"