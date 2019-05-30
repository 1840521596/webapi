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
class course_schemaTest(unittest.TestCase):
    #"course_schema"
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
    
    def test_01_course_index(self):
        """课程体系"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/coursedetail.htm?url=https://resource.yunshuxie.com/dailySentence/sale/sale-daily-clock2018.html"
        method = "GET"
        caseHeaders = {"Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        respMsg = self.resp.content  #返回值
        caseExpectDatas = self.caseExpectDatas  #xls 校验值
        if caseExpectDatas:
            if type(caseExpectDatas).__name__ == "str":
                assert caseExpectDatas==respMsg,msg.format(Except=caseExpectDatas,Really=respMsg)
            elif type(caseExpectDatas).__name__ == "dict":
                json_caseExpectDatas = json.dumps(caseExpectDatas, encoding='utf-8', ensure_ascii=False)  # 期望值转换json
                try:
                    dict_resp = json.loads(re.match(".*?({.*}).*", respMsg, re.S).group(1))
                    assert caseExpectDatas==dict_resp,msg.format(Except=json_caseExpectDatas, Really=respMsg)  #判断期望值==返回值(转换成字典)
                except Exception as e:  #当value2 不是json类型
                    print e
                    respMsg = re.match(".*?({.*}).*", respMsg, re.S).group(1)
                    assert json_caseExpectDatas == respMsg,msg.format(Except=json_caseExpectDatas, Really=respMsg)

    def test_02_get_token(self):
        """课程体系-get_token"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":{"sign":"be493a88dee3c26b386cda409ffee407","ts":"1554961282012","token":"a4fdcb28fb5b4e20afe13b8278ae28ac"}}
        params = {"callback":" jQuery22405451987913863958_1554961284267","vid": "eaceb0a5eaf05970eecfe1a194889bd0_e","_": "1554961284268"}
        self.url = "https://wap.yunshuxie.com"+"/v1/video_public/get_token.htm"
        method = "GET"
        caseHeaders = {"Referer": "https://resource.yunshuxie.com/dailySentence/sale/sale-daily-clock2018.html?comefrom=pc","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
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
    def test_03_OneDayOneWord_mp4(self):
        """每日一句课程视频介绍"""
        self.caseStatusCode = 206
        self.caseExpectDatas =None
        params = {"pid": "1554964032622X1261191"}
        self.url = "https://dpv.videocc.net"+"/eaceb0a5ea/0/eaceb0a5eaf05970eecfe1a194889bd0_2.mp4"
        method = "GET"
        caseHeaders = {"Accept-Encoding": "identity;q=1, *;q=0","Range": "bytes=425984-","Referer": "https://resource.yunshuxie.com/dailySentence/sale/sale-daily-clock2018.html?comefrom=pc","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_04_OneDayOneWord_mp3(self):
        """每日一句课程音频介绍"""
        self.caseStatusCode = 206
        self.caseExpectDatas =None
        params = None
        self.url = "https://oss-ysx-pic.yunshuxie.com"+"/course/2017/12/27/14/1514356711784.mp3"
        method = "GET"
        caseHeaders = {"Accept-Encoding": "identity;q=1, *;q=0","Range": "bytes=65536-","Referer": "https://resource.yunshuxie.com/dailySentence/sale/sale-daily-clock2018.html?comefrom=pc","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
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