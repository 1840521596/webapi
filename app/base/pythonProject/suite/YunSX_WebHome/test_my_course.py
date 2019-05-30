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
class my_courseTest(unittest.TestCase):
    #"my_course"
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
    
    def test_01_course_sign(self):
        """每日签到"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":{"totalPowerValue":"2","code":"1","powerValue":"1","msg":"签到成功","continueTime":"1"}}
        params = {"memberId": "1287384","callback": "_jsonpvermzoxz18s"}
        self.url = "https://www.yunshuxie.com"+"/v1/checkIn/insertCheckIn.htm?memberId=1287384&callback=_jsonpvermzoxz18s"
        method = "GET"
        caseHeaders = {"Referer":"https://resource.yunshuxie.com/home/mine/views/index_V2.html","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
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
    def test_02_course_quxian(self):
        """获取区县地址"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":[{"districtName":"东城区","districtId":"110101","cityId":"110000","sortCode":"0"},{"districtName":"西城区","districtId":"110102","cityId":"110000","sortCode":"0"},{"districtName":"朝阳区","districtId":"110105","cityId":"110000","sortCode":"0"},{"districtName":"丰台区","districtId":"110106","cityId":"110000","sortCode":"0"},{"districtName":"石景山区","districtId":"110107","cityId":"110000","sortCode":"0"},{"districtName":"海淀区","districtId":"110108","cityId":"110000","sortCode":"0"},{"districtName":"门头沟区","districtId":"110109","cityId":"110000","sortCode":"0"},{"districtName":"房山区","districtId":"110111","cityId":"110000","sortCode":"0"},{"districtName":"通州区","districtId":"110112","cityId":"110000","sortCode":"0"},{"districtName":"顺义区","districtId":"110113","cityId":"110000","sortCode":"0"},{"districtName":"昌平区","districtId":"110114","cityId":"110000","sortCode":"0"},{"districtName":"大兴区","districtId":"110115","cityId":"110000","sortCode":"0"},{"districtName":"怀柔区","districtId":"110116","cityId":"110000","sortCode":"0"},{"districtName":"平谷区","districtId":"110117","cityId":"110000","sortCode":"0"},{"districtName":"密云区","districtId":"110228","cityId":"110000","sortCode":"0"},{"districtName":"延庆区","districtId":"110229","cityId":"110000","sortCode":"0"}]}
        params = {"callback":"_jsonpnfc9fbn9u3"}
        self.url = "https://www.yunshuxie.com"+"/v1/web/class/bjDistrictList.json?callback=_jsonpnfc9fbn9u3"
        method = "GET"
        caseHeaders = {"Referer":"https://resource.yunshuxie.com/home/mine/views/index_V2.html","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
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

    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        
        pass
if __name__ == "__main__":
    unittest.main()