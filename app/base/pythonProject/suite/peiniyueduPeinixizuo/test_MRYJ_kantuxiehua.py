#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
import redis
# sys.path.append("../../base")
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
logging = TestLog().getlog()
class KanTuXieHua_Test(unittest.TestCase):
    """看图写话60讲->销售查询->系统时间->查询课程信息->查询优惠券-><br/>课程购买查询->发送验证码->校验验证码->个人购买全期课程"""
    globals_values = ""
    @classmethod
    def setUpClass(self):
        self.s = ReadConfig()
        self.env_flag = self.s.get_env("env_flag")
        self.env_num = self.s.get_env("env_num")
        self.phonenum = self.s.get_params("phonenum")
        self.session = requests.Session()
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount("https://", request_retry)
        self.session.mount("http://", request_retry)
        header = {"Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded","Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
        self.session.headers = header
        cookies = {"env_flag": self.env_flag, "env_num": self.env_num}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.pattern = "{\"global.*}"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        globals()["resp_value"] = ""
    def test_01_query_saleman(self):
        """https://pay.yunshuxie.com/v6/order/query/saleman.htm<br/>"{"sk":"null","callback":"Zepto1558926534750"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/saleman.htm"
        params = {"sk":"null","callback":"Zepto1559011256180"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)
        print "查询销售人员:"+resp.content +"<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "15", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result["returnCode"] == "15" or result["returnCode"] == 15
        assert result.has_key("returnMsg")
        assert result.has_key("data")
    def test_02_common_api_date(self):
        """https://wap.yunshuxie.com/v1/common/api/date.htm<br/>{"callback":"Zepto1559011256179"}"""
        url = r"https://wap.yunshuxie.com/v1/common/api/date.htm"
        params = {"callback":"Zepto1559011256179"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url, params=params)
        print "查询系统时间:" + resp.content + "<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["date"] != ""
        assert result.has_key("timestamp")
        assert result["timestamp"] != ""
    def test_03_query_basic_course_id(self):
        """https://pay.yunshuxie.com/v6/basicCourse/query/basic_course_id.htm<br/>{"cType":"73","callback":"Zepto1559011256181"}"""
        url = r"https://pay.yunshuxie.com/v6/basicCourse/query/basic_course_id.htm"
        params = {"cType":"73","callback":"Zepto1559011256181"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)
        print "课程信息查询:" + resp.content + "<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "0", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result["returnCode"] == "0" or result["returnCode"] == 0
        assert result.has_key("returnMsg")
        assert result.has_key("data")
        values = [[course["productCourseHoursId"],course["productId"]] for course in result["data"]]
        globals()["globals_values"] = values
    def test_04_coupon_query_use_list(self):
        """https://pay.yunshuxie.com/v2/coupon/query/use_list.htm<br/>{"phone":phonenum,"productId":"7485","activityType":"-1","callback":"__jp1"}"""
        url = r"https://pay.yunshuxie.com/v1/coupon/query/use_list.htm"
        params = {"phone":self.phonenum,"productId":"7485","activityType":"-1","callback":"__jp1"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)
        print "优惠券查询:" + resp.content + "<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "0", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result["returnCode"] == "0" or result["returnCode"] == 0
        assert result.has_key("returnMsg")
        assert result.has_key("data")
    def test_05_query_repeat_purchase(self):
        """https://pay.yunshuxie.com/v6/order/query/repeat_purchase.htm<br/> {"phone":phonenum,"pId":"7485","callback":"__jp8"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/repeat_purchase.htm"
        params = {"phone":self.phonenum,"pId":"7485","callback":"__jp8"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url, params=params)
        print "课程是否购买查询:" + resp.content + "<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "0", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert result["returnCode"] == "0" or result["returnCode"] == 0
        assert result.has_key("returnMsg")
        assert result["data"] != {}
        assert result.has_key("data")
    def test_06_wap_getValidate(self):
        """https://account.yunshuxie.com/v1/validate/wap/getValidate.htm<br/>{"phone":phonenum,"callback":"Zepto1558929540208"}"""
        url = r"https://account.yunshuxie.com/v1/validate/wap/getValidate.htm"
        params = {"phone":self.phonenum,"callback":"__jp10"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  #发送验证码
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "发送验证码:"+resp.content +"<br/>"
        expect = {"code":"0"}
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],Really=result["code"])
    def test_07_wap_validateKey(self):
        """https://account.yunshuxie.com/v1/validate/wap/validateKey.htm<br/>{"phone":phonenum,"validate":captcah,"callback":"Zepto1558929540208","activityId":""}"""
        self.redis_host = self.s.get_env("beta").split(":") if self.env_flag == "beta" else self.s.get_env("prod_stage").split(":")
        r = redis.Redis(host=self.redis_host[0], port=int(self.redis_host[1]), password="yunshuxie1029Password")
        redis_shell = "code_5_"+self.phonenum
        captcah = r.get(redis_shell)
        url = r"https://account.yunshuxie.com/v1/validate/wap/validateKey.htm"
        params = {"phone":self.phonenum,"validate":captcah,"callback":"Zepto1558929540208","activityId":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  #发送验证码
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "获取验证码{capth}:".format(capth=captcah) + resp.content +"<br/>"
        expect = {"code":"0"}
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],Really=result["code"])
    def test_08_order_create(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/>{"phone":"phoneNum,"customizeGroupId":"-1","phId":productCourseHoursId,<br/>"gId":"-1",pId": productId,"pType": "1","productType": "73","channelId": "AliPay",<br/>"cSn":"","sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        for productCourseHoursId,productId  in globals_values:
            url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
            params = {"phone": "{}".format(self.phonenum),"customizeGroupId": "-1","phId": productCourseHoursId,"gId": "-1",
                  "pId": productId,"pType": "1","productType": "73","channelId": "AliPay",
                  "cSn": "","sk": "","grade": "","addressId": "-1","activityId": "-1"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            resp = self.session.get(url=url,params=params)
            print "课程购买【phId】：{phId}--【pId】：{pId}:".format(phId=productCourseHoursId,pId=productId) + resp.content + "<br/>"
            logging.info(url + lianjiefu + resp.text + fengefu)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        del globals()["resp_value"]
if __name__ == "__main__":
    unittest.main()