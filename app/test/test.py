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

# ########################## 消费者 ##########################
credentials = pika.PlainCredentials('admin', 'admin')
# 连接到rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.1.194',5672,'/',credentials))
channel = connection.channel()

# 声明消息队列，消息将在这个队列中进行传递。如果队列不存在，则创建
channel.queue_declare(queue='wzg')


# 定义一个回调函数来处理，这边的回调函数就是将信息打印出来。
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# 告诉rabbitmq使用callback来接收信息
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
 # no_ack=True表示在回调函数中不需要发送确认标识

print(' [*] Waiting for messages. To exit press CTRL+C')

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出。
channel.start_consuming()