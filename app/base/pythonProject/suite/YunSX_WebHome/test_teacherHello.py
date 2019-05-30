#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from requests import Session,Request
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
logging = TestLog().getlog()
class teacherHelloTest(unittest.TestCase):
    #"teacherHello"
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        env_flag = s.get_env("env_flag")
        env_num = s.get_env("env_num")
        phoneNum = s.get_params("phoneNum")
        userName = s.get_admin("userName")
        pwd = s.get_admin("pwd")
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('env_flag', env_flag)  #设置测试环境
        self.cookies.set("env_num",env_num)  #设置环境号
        
        data = {"userName":"13500000023","pwd":"123456"}
        self.url = "https://www.yunshuxie.com"+"/v5/web/account/login.htm"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.post(self.url, data=data, headers=caseHeaders ,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        self.cookies.update(self.resp.cookies)
    
    def test_01_praise(self):
        """点赞"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":"4"}
        params = {"activityId":"3020","commentId":"229869","type":"1"}
        self.url = "https://msg.yunshuxie.com"+"/v5/activity/comment/addPraise.htm"
        method = "GET"
        caseHeaders = {"Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        def assertKey(value1,value2):
            dictvalue1 = value1
            dictvalue2 = value2
            if type(dictvalue2).__name__ == "dict":
                for key,value in dictvalue2.items():
                    if dictvalue1.has_key(key):
                        if type(value).__name__ == "dict":
                            assertKey(dictvalue1[key],dictvalue2[key])
                        elif type(value).__name__ == "list":
                            assertKey(dictvalue1[key],dictvalue2[key])
                    else:
                        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""
                        return key
            elif type(dictvalue2).__name__ == "list":
                for list_index in range(len(dictvalue2)):
                    assertKey(dictvalue1[list_index],dictvalue2[list_index])
        value1 = self.caseExpectDatas
        value2 = json.loads(re.match(".*?({.*}).*", self.resp.content, re.S).group(1))
        keyValue = assertKey(value1,value2)
        if keyValue:
            assert keyValue=="Error",msg.format(Except=keyValue,Really="Error")
    def test_02_praise_again(self):
        """点赞"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":"4"}
        params = {"activityId":"3020","commentId":"229869","type":"1"}
        self.url = "https://msg.yunshuxie.com"+"/v5/activity/comment/addPraise.htm"
        method = "GET"
        caseHeaders = {"Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        def assertKey(value1,value2):
            dictvalue1 = value1
            dictvalue2 = value2
            if type(dictvalue2).__name__ == "dict":
                for key,value in dictvalue2.items():
                    if dictvalue1.has_key(key):
                        if type(value).__name__ == "dict":
                            assertKey(dictvalue1[key],dictvalue2[key])
                        elif type(value).__name__ == "list":
                            assertKey(dictvalue1[key],dictvalue2[key])
                    else:
                        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""
                        return key
            elif type(dictvalue2).__name__ == "list":
                for list_index in range(len(dictvalue2)):
                    assertKey(dictvalue1[list_index],dictvalue2[list_index])
        value1 = self.caseExpectDatas
        value2 = json.loads(re.match(".*?({.*}).*", self.resp.content, re.S).group(1))
        keyValue = assertKey(value1,value2)
        if keyValue:
            assert keyValue=="Error",msg.format(Except=keyValue,Really="Error")
    def test_03_praise_again1(self):
        """点赞"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":"4"}
        params = {"activityId":"3020","commentId":"229869","type":"1"}
        self.url = "https://msg.yunshuxie.com"+"/v5/activity/comment/addPraise.htm"
        method = "GET"
        caseHeaders = {"Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        def assertKey(value1,value2):
            dictvalue1 = value1
            dictvalue2 = value2
            if type(dictvalue2).__name__ == "dict":
                for key,value in dictvalue2.items():
                    if dictvalue1.has_key(key):
                        if type(value).__name__ == "dict":
                            assertKey(dictvalue1[key],dictvalue2[key])
                        elif type(value).__name__ == "list":
                            assertKey(dictvalue1[key],dictvalue2[key])
                    else:
                        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""
                        return key
            elif type(dictvalue2).__name__ == "list":
                for list_index in range(len(dictvalue2)):
                    assertKey(dictvalue1[list_index],dictvalue2[list_index])
        value1 = self.caseExpectDatas
        value2 = json.loads(re.match(".*?({.*}).*", self.resp.content, re.S).group(1))
        keyValue = assertKey(value1,value2)
        if keyValue:
            assert keyValue=="Error",msg.format(Except=keyValue,Really="Error")
    def test_04_praise_again2(self):
        """点赞"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":"3"}
        params = {"activityId":"3020","commentId":"229869","type":"-1"}
        self.url = "https://msg.yunshuxie.com"+"/v5/activity/comment/addPraise.htm"
        method = "GET"
        caseHeaders = {"Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        
        pass
if __name__ == "__main__":
    unittest.main()