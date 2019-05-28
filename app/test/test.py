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

username = 'admin'#指定远程rabbitmq的用户名密码
pwd = 'ysx@1ppt'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.1.183', port=5672,credentials=user_pwd))#创建连接
chan = s_conn.channel()#在连接上创建一个频道

chan.queue_declare(queue='HA_wxOrderQueue')#声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行


def callback(ch,method,properties,body): #定义一个回调函数，用来接收生产者发送的消息
    print("[消费者] recv %s" % body)

chan.basic_consume(callback,  #调用回调函数，从队列里取消息
                   queue='HA_wxOrderQueue',#指定取消息的队列名
                   no_ack=True) #取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可
print('[消费者] waiting for msg .')
chan.start_consuming()#开始循环取消息