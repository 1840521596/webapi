#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
import urllib
from requests_toolbelt import MultipartEncoder
#sys.path.append("/app/base/pythonProject/base")
#sys.path.append("../../base")
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
from getCrmCookies import get_crm_cookie
logging = TestLog().getlog()
class Ysx_Make_User(unittest.TestCase):
    """短信服务"""
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        self.env_flag = s.get_env("env_flag")
        self.env_num = s.get_env("env_num")
        self.phoneNumList =  s.get_params("phonenumlist")
        self.employeeTypes = s.get_params("employeetypes")
        self.userNames = ",".join(["测试_"+userName for userName in self.phoneNumList.split(",")])
        self.admin_pwd = s.get_admin("pwd")
        self.admin_usernmae = s.get_admin("username")
        self.session = requests.Session()
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount("https://", request_retry)
        self.session.mount("http://", request_retry)
        cookie_dict = {'env_flag':self.env_flag,"env_num":self.env_num}  #设置环境号
        #cookie_dict = {'env_flag':"beta","env_num":"2"}  #设置环境号
        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        self.session.cookies = cookies
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.session.headers = self.header
        self.salt = "mengmengda"
        self.msg = """\n        Except:  {Except}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
    def test_01_make_user(self):
        """make_user_admin平台创建测试用户
        """
        url = r"https://www.yunshuxie.com"+"/v5/web/account/login.htm"
        data = {"userName": self.admin_usernmae, "pwd": self.admin_pwd}
        self.resp = self.session.post(url, data=data)  # 登录admin测试环境,记录cookies
        url = r"https://admin.yunshuxie.com/v1/admin/account/add/user.json"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","X-Requested-With": "XMLHttpRequest","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cache-Control": "no-cache","Connection": "keep-alive","Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryF7Lcp4O5PcTcLugw"}
        userName = ["测试_"+userName for userName in self.phoneNumList.split(",")]
        userPhone = self.phoneNumList.split(",")
        employeeTypes = self.employeeTypes.split(",")
        for index in range(len(userName)):
            datas = {"memberIcon": "", "pwd": "123456", "email": "automation@yunshuxie.com", "weiboName": "",
                     "nickName": userName[index], "qq": "", "interest": "", "phone":userPhone[index] , "weichatNum": "",
                     "remark": "自动化测试", "memberType": employeeTypes[index], "ChoiceOfTeacher": "默认分组", "ChoiceOfTeacher": "默认分组",
                     "readRole": "0", "ChoiceOfTeacher": "云舒写教育科技", "button": ""}
            data = MultipartEncoder(datas)
            headers["Content-Type"] = data.content_type
            self.session.headers = headers
            logging.info(url + lianjiefu + json.dumps(datas,ensure_ascii=False) + fengefu)
            self.resp = self.session.post(url, data=data)
            print self.resp.content
            logging.info(url + lianjiefu + self.resp.text + fengefu)
            result = json.loads(self.resp.content)
            assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
    def test_02_add_TestUser(self):
        """make_user_CRM平台备注测试用户
        """
        url = r"http://admin.crm.yunshuxie.com/test/account/management/insert/test/account"
        cookies = get_crm_cookie(self.env_flag,self.env_num)
        headers = {"Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate","Accept-Language": "zh-CN,zh;q=0.9","Cache-Control": "no-cache","Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Pragma": "no-cache","Referer": "http://admin.crm.yunshuxie.com/test/account/management/goto/insert/test/account","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
        self.session.headers = headers
        self.session.cookies = cookies
        for phone in self.phoneNumList.split(","):
            data = {"phones": phone ,"userNames": "测试_{phone}".format(phone=phone),"employeeTypes": 0}
            logging.info(url + lianjiefu + json.dumps(data,ensure_ascii=False) + fengefu)
            self.resp = self.session.post(url, data=data)
            print self.resp.content
            logging.info(url + lianjiefu + self.resp.text + fengefu)
            result = json.loads(self.resp.content)
            assert result["returnCode"] == 0,self.msg.format(Except="0",Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        pass
if __name__ == "__main__":
    unittest.main()