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

s= {"rows": [
    {"commemtId": 210189, "timeLineId": 1953109, "phone": "18811063258", "gagType": 1, "timeLineStatus": 1,
     "title": "[2年级-18.12]查理和巧克力工厂:导读任务四", "createDate": "2019-01-06 11:52:37",
     "tcontent": "老师好，今天上传《查理和巧克力工厂》最后一次作业，请老师点评第一人称写的《坏了的核桃》，谢谢老师。", "memberId": 1014682,
     "commentupdateDate": "2019-04-24 11:51:09", "content": "哈哈", "nickName": "外婆高"},
    {"commemtId": 196722, "timeLineId": 1805593, "phone": "18811063258", "gagType": 1, "timeLineStatus": 0,
     "title": "【名著精读】鲁滨逊漂流记", "createDate": "2018-12-17 12:34:33", "tcontent": "不会", "memberId": 1014682,
     "content": "加油", "nickName": "外婆高"}], "total": 2, "limit": 20}
b ={"rows": [
    {"content": "哈哈", "title": "[2年级-18.12]查理和巧克力工厂:导读任务四", "phone": "18811063258", "nickName": "外婆高",
     "tcontent": "老师好，今天上传《查理和巧克力工厂》最后一次作业，请老师点评第一人称写的《坏了的核桃》，谢谢老师。", "commemtId": 210189,
     "commentupdateDate": "2019-06-03 14:31:54", "timeLineStatus": 1, "gagType": 1, "memberId": 1014682,
     "timeLineId": 1953109, "createDate": "2019-01-06 11:52:37"},
    {"content": "加油", "title": "【名著精读】鲁滨逊漂流记", "phone": "18811063258", "nickName": "外婆高", "tcontent": "不会",
     "commemtId": 196722, "timeLineStatus": 0, "gagType": 1, "memberId": 1014682, "timeLineId": 1805593,
     "createDate": "2018-12-17 12:34:33"}], "total": 2, "limit": 20}
print s["rows"]==b["rows"]

print s["rows"][0]
print b["rows"][0]
