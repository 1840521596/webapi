#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from bs4 import BeautifulSoup
import time
import sys
#sys.path.append("./app/base/pythonProject/base")
#sys.path.append("../../base")
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
logging = TestLog().getlog()
class JingPinKeCheng_Test(unittest.TestCase):

    """每日积累"""
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        env_flag = s.get_env("env_flag")
        env_num = s.get_env("env_num")
        self.phoneNum = s.get_params("phoneNum")
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('env_flag', env_flag)  #设置测试环境
        self.cookies.set("env_num",env_num)  #设置环境号
        self.headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15565269850789002 webdebugger port/34092"}
        ysx_JingPinHaoKe_url = r"https://c.yunshuxie.com/class_all.html"
        self.resp = requests.get(url= ysx_JingPinHaoKe_url, headers= self.headers,cookies= self.cookies)
        logging.info(ysx_JingPinHaoKe_url + lianjiefu + self.resp.text +fengefu )
        self.cookies.update(self.resp.cookies)
        pattern = "{\"global.*}"
        self.result = re.findall(pattern, self.resp.content)[0]
        self.course_info = json.loads(self.result, encoding="utf8")["class_all"]["response"]["data"]["productList"]
       # productList = filter(lambda course: [m for m in course if m["productType" == u"每日一句"]],
        #                     self.course_info[1])  # 提取每日一句
        self.productDict = {}
        for  list_course in self.course_info:
            self.list_course = []
            for course in list_course:
                #print course["productType"]
                if course["productType"] == u"每日一句":
                    #print course["productName"]
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                elif course["productType"] == u"名著读写线上课":
                    # print course["productName"]
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                elif course["productType"] == u"名著读写面授课":
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                elif course["productType"] == u"应试必备课程":
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                self.list_course.append(self.productList )
            self.productDict[course["productType"]] =self.list_course
            #[{"saleUrl": url ,"productName": str ,"resp": html }]
        self.msg = """\n        Except:  {Except}-*-\n        Really:  {Really}"""  #校验HTTP返回代码



    def test_4_MRYJ_xiaoxuegaofenzuowenbihuichengyuku(self):
        """每日一句 - -《小学高分作文必会成语课》课程信息-个人购买"""
        for project in self.productDict[u"每日一句"]:
            for course_info in project:
                if course_info["productName"] == u"小学高分作文必会成语课":
                    self.resp = requests.get(course_info["saleUrl"], headers=self.headers, cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + self.resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"], headers=self.headers,
                                                       cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"], headers=self.headers,
                                                     cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert self.resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200
                    url = r"https://pay.yunshuxie.com/v6/basicCourse/query/basic_course_id.htm"
                    params = {"cType":"72","_":"1557217121011","callback":"Zepto1557217118071"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    productCourseHoursId = result["data"][0]["productCourseHoursId"]  # 选择课程，默认第一个
                    productId = result["data"][0]["productId"]  # 选择课程，默认第一个
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    url = r"https://wap.yunshuxie.com/v1/common/api/date.htm"
                    params = {"_":"1557217120957","callback":"Zepto1557217118069"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)  # 进行时间比对
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    today = time.localtime(time.time())
                    assert result["date"][:10] == time.strftime('%Y-%m-%d',
                                                                today ) , self.msg.format(Except=today,
                                                                                    Really=result["date"][:10])  #判断接口返回时间 == 系统时间(精确到day)
                    url = r"https://pay.yunshuxie.com/v1/h5_share/query/signature_jsonp.htm"
                    params = {"url":"https://pay.yunshuxie.com/H5Pay/sale_watchImgWriting/index.html","_":"1557209606715","callback":"Zepto1557209606557"}
                    signature_jsonp_resp = requests.get(url=url, params=params, headers=self.headers, cookies=self.cookies)
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone={phone}&type=2".format(phone=self.phoneNum)
                    self.resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"}
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
                    params = {"phone": "{}".format(self.phoneNum),"customizeGroupId": "-1",
                              "phId": productCourseHoursId,"gId": "-1","pId": productId,"pType": "1","productType": 72,
                              "channelId": "AliPay","cSn": "","sk": "","grade": "4","addressId": "-1","activityId": "-1"}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url,headers=headers,params=params,cookies=self.cookies)
                    print self.resp.content
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(self.resp.content, encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
    def test_5_MZDXXSK_ywhxsysjzbk(self):
        """名著读写线上课 - -《语文核心素养暑期直播课》课程信息-个人购买"""
        for project in self.productDict[u"名著读写线上课"]:
            for course_info in project:
                if course_info["productName"] == u"语文核心素养暑期直播课":
                    self.resp = requests.get(course_info["saleUrl"], headers=self.headers, cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + self.resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"], headers=self.headers,
                                                       cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"], headers=self.headers,
                                                     cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert self.resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200
                    url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerPrice.htm"
                    params = {"pt":"-1","_":"1557217121011","callback":"Zepto1557307951251"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    productId = result["data"][0]["productId"]  # 选择课程，默认第一个  7652
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerGrade.htm"
                    params = {"productId":productId,"_":"1557217120957","callback":"Zepto1557308333255"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    grade = result["data"][0]["grade"]   # 选择年级，默认第一个  ,3,
                    url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerCourse.htm"
                    params = {"productId": productId,"grade":grade, "_": "1557217120957", "callback": "Zepto1557308333258"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    productCourseHoursId = result["data"][0][0]["productCourseHoursId"]
                    url= r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerPay.htm"
                    params = {"phone":self.phoneNum,"productId":productId,"grade":grade,"callback":"__jp1"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone={phone}&type=2".format(phone=self.phoneNum)
                    self.resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"}
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
                    params = {"phone":self.phoneNum,"phId":productCourseHoursId,"gId":"-1","productId":productId,
                              "pType":"1","productType":"76","channelId":"AliPay","cSn":"","sk":"",
                              "grade":grade,"customizeGroupId":"","addressId":"-1","activityId":"-1"}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url,headers=headers,params=params,cookies=self.cookies)
                    print self.resp.content
                    logging.info(url + lianjiefu + json.dumps(params) + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(self.resp.content, encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
    def test_6_MZDXXSK_mzjdk(self):
        """名著读写线上课 - -《名著精读课》课程信息-个人购买"""
        for project in self.productDict[u"名著读写线上课"]:
            for course_info in project:
                if course_info["productName"] == u"名著精读课":
                    saleUrl_resp = requests.get(url=course_info["saleUrl"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + saleUrl_resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert saleUrl_resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200

                    url = r"https://pay.yunshuxie.com/v5/h5_christmas/query/activity.htm"
                    params = {"productType":"2"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    url = r"https://wap.yunshuxie.com/v1/member_standard_product/get_member_standard_detailv2.json"
                    params = {"memberCourseType":"1","type":"1","memberGrade":"1","week":"7","phone":self.phoneNum,"callback":"__jp0"}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    phIds = result["data"]["courseList"][0]["productHoursId"]  #  获取课程productHoursId
                    productId = result["data"]["courseList"][0]["productId"]  #  获取课程productId
                    url = r"https://pay.yunshuxie.com/v6/order/order_param.htm"
                    params = {"memberCourseType": "1","type":"1", "memberGrade": "1", "callback": "__jp0","phone":self.phoneNum,"phIds":phIds}
                    self.resp = requests.get(url=url, headers=self.headers, params=params, cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone=18900000017&type=2"
                    account_resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"
                    url= r"https://pay.yunshuxie.com/v6/order/create2.htm"
                    params = {"phone":self.phoneNum,"pIds":productId,"phIds":phIds,"pType":"1","productType":"1","memberCourseType":"1",
                              "type":"1","memberGrade":"1","sk":"","cSn":"","addressId":"-1","activityId":"-1",
                              "customizeGroupId":"-1","channelId":"AliPay"}
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url, headers=headers, params=params, cookies=self.cookies)
                    print self.resp.content
                    assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
    def test_7_MZDXXSK_xzxtk(self):
        """名著读写线上课 - -《写作系统课》课程信息-个人购买"""
        for project in self.productDict[u"名著读写线上课"]:
            for course_info in project:
                if course_info["productName"] == u"写作系统课":
                    self.resp = requests.get(course_info["saleUrl"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + self.resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert self.resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone={phone}&type=2".format(phone=self.phoneNum)
                    account_resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"}
                    logging.info(url + lianjiefu + account_resp.text + fengefu)
                    url = r"https://wap.yunshuxie.com/v1/member_standard_product/get_member_standard_detailv2.json"
                    params = {"memberCourseType":"2","type":"1","memberGrade":"3","phone":self.phoneNum,"callback":"__jp0"}
                    self.resp = requests.get(url=url,headers=self.headers,params=params,cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
                    url = r"https://pay.yunshuxie.com/v6/order/order_param.htm"
                    productHoursId = result["data"]["courseList"][0]["productHoursId"]
                    productId = result["data"]["courseList"][0]["productId"]
                    params = {"memberCourseType":"2","type":"1","phIds":productHoursId,"memberGrade":"3","phone":self.phoneNum}
                    url = r"https://pay.yunshuxie.com/v6/order/create2.htm"
                    params = {"phone":self.phoneNum,"pIds":productHoursId,"phIds":productId,
                              "pType":"1","productType":"1","memberCourseType":"2","type":"1","channelId":"AliPay",
                              "memberGrade":"3","sk":"null","cSn":"","addressId":"-1","activityId":"-1","customizeGroupId":"-1"}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url,headers=headers,params=params ,cookies=self.cookies)   #生成支付订单
                    print self.resp.content
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
    def test_8_MZDXXSK_zwydyjpxgk(self):
        """名著读写线上课 - -《作文一对一精批细改课》课程信息-个人购买"""
        for project in self.productDict[u"名著读写线上课"]:
            for course_info in project:
                if course_info["productName"] == u"作文一对一精批细改课":
                    self.resp = requests.get(course_info["saleUrl"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + self.resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert self.resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200
                    url = r"https://pay.yunshuxie.com/v6/order/query/product_course.htm"
                    params = {"grade":"3","callback":"Zepto1557730451559"}
                    self.resp = requests.get(url=url,headers=self.headers,params=params,cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
                    productCourseHoursId = result["data"][0]["productCourseHoursId"]
                    productCourseId = result["data"][0]["productCourseId"]
                    productId = result["data"][0]["productId"]
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone={phone}&type=2".format(phone=self.phoneNum)
                    account_resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"}
                    logging.info(url + lianjiefu + account_resp.text + fengefu)
                    url = r"https://pay.yunshuxie.com/v6/order/query/product_price.htm"
                    params = {"phone":self.phoneNum,"pId":productId,"callback":"__jp2"}
                    self.resp = requests.get(url=url,headers=self.headers,params=params,cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    url = "https://pay.yunshuxie.com/v6/order/create.htm"
                    params = {"phone":self.phoneNum,"pIds":productCourseHoursId,"gId":"-1",
                              "pId":productId,"pType":"1","productType":"66","type":"1","channelId":"AliPay",
                              "grade":"三年级","sk":"null","cSn":"","addressId":"-1"}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url,headers=headers,params=params ,cookies=self.cookies)   #生成支付订单
                    print self.resp.content
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        pass
if __name__ == "__main__":
    unittest.main()