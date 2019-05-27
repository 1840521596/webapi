#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
import redis
# sys.path.append("./app/base/pythonProject/base")
# sys.path.append("../../base")
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
logging = TestLog().getlog()
class MeiRiYiJuGuShiWen_Test(unittest.TestCase):
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
        cookies = {"env_flag": "prod", "env_num": ""}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.pattern = "{\"global.*}"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        globals()["resp_value"] = ""
    def test_01_query_saleman(self):
        """https://pay.yunshuxie.com/v6/order/query/saleman.htm<br/>"{"sk":"null","callback":"Zepto1558926534750"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/saleman.htm"
        params = {"sk":"null","callback":"Zepto1558926534750"}
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
    def test_02_coupon_query_use_list(self):
        """https://pay.yunshuxie.com/v2/coupon/query/use_list.htm<br/>{"phone":self.phonenum,"productId":"2845","couponType":"1",</br>"activityId":"118","activityType":"1","memberType":"0","callback":"Zepto1558942898195"}"""
        url = r"https://pay.yunshuxie.com/v2/coupon/query/use_list.htm"
        params = {"phone":self.phonenum,"productId":"2845","couponType":"1","activityId":"118","activityType":"1","memberType":"0","callback":"Zepto1558942898195"}
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
    def test_03_wap_getValidate(self):
        """https://account.yunshuxie.com/v1/validate/wap/getValidate.htm<br/>{"phone":self.phonenum,"callback":"Zepto1558929540208"}"""
        url = r"https://account.yunshuxie.com/v1/validate/wap/getValidate.htm"
        params = {"phone":self.phonenum,"callback":"Zepto1558929540208"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  #发送验证码
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "发送验证码:"+resp.content +"<br/>"
        expect = {"code":"0"}
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],Really=result["code"])
    def test_04_wap_validateKey(self):
        """https://account.yunshuxie.com/v1/validate/wap/validateKey.htm<br/>{"phone":self.phonenum,"validate":captcah,"callback":"Zepto1558929540208","activityId":""}"""
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
    def test_05_get_create_order(self):
        """get_create_order<br/>一年级及学前:<br/>{"phone":self.phonenum, "productId": "2845", "phId": "2854",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "2845", "phId": "2854",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《一年级及学前》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_06_get_create_order(self):
        """get_create_order<br/>二年级:<br/>{"phone":self.phonenum, "productId": "2846", "phId": "2855",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "2846", "phId": "2855",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《二年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_07_get_create_order(self):
        """get_create_order<br/>三年级:<br/>{"phone":self.phonenum, "productId": "2847", "phId": "2856",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "2847", "phId": "2856",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《三年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_08_get_create_order(self):
        """get_create_order<br/>四年级:<br/>{"phone":self.phonenum, "productId": "3021", "phId": "2998",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "3021", "phId": "2998",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《四年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_09_get_create_order(self):
        """get_create_order<br/>五年级:<br/>{"phone":self.phonenum, "productId": "3022", "phId": "2999",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "3022", "phId": "2999",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《五年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_10_get_create_order(self):
        """get_create_order<br/>六年级:<br/>{"phone":self.phonenum, "productId": "3023", "phId": "3000",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "3023", "phId": "3000",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《六年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_11_get_create_order(self):
        """get_create_order<br/>七年级:<br/>{"phone":self.phonenum, "productId": "3024", "phId": "3001",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "3024", "phId": "3001",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《七年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_12_get_create_order(self):
        """get_create_order<br/>八九年级:<br/>{"phone":self.phonenum, "productId": "3025", "phId": "3002",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone":self.phonenum, "productId": "3025", "phId": "3002",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《八九年级》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    def test_13_get_create_order(self):
        """get_create_order<br/>高中:<br/>{"phone":self.phonenum, "productId": "3026", "phId": "3003",<br/>"code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",<br/>"activityId": "-1", "cSn": ""}"""
        url = r"https://pay.yunshuxie.com/v4/order/h5_pay/DS/post/get_create_order.htm"
        params = {"phone": self.phonenum, "productId": "3026", "phId": "3003",
                  "code": "o38sIv_7FQInsBKJEUExn7wYxoHc", "sk": "null", "agentId": "", "customizeGroupId": "-1",
                  "activityId": "-1", "cSn": ""}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url, params=params)  # 生成支付订单
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "《高中》购买:"+resp.content +"<br/>"
        result = json.loads(resp.content, encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Except="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Except=resp.content, Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        del globals()["resp_value"]
if __name__ == "__main__":
    unittest.main()