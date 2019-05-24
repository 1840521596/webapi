#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
# import sys
# sys.path.append("../../base")
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
from getCrmCookies import get_crm_cookie
logging = TestLog().getlog()
class Ysx_Crm_CXSHDD(unittest.TestCase):
    """CRM 查询商户订单"""
    @classmethod
    def setUpClass(self):
        s = ReadConfig()
        env_flag = s.get_env("env_flag")
        env_num = s.get_env("env_num")
        self.session = requests.Session()
        #cookies = get_crm_cookie("beta","2")
        cookies = get_crm_cookie(env_flag,env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Upgrade-Insecure-Requests": "1"}
        self.msg = """\n        Except:  {Except}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_01_merchants_order(self):
        """查询商户订单<br/> {"sort": "nowDate","order": "asc","limit": "3",<br/>"offset": "0","_": "1558510544182"}
        """
        url = r"http://admin.crm.yunshuxie.com/v1/admin/order/query/merchants/order"
        params = {"orderSn": "Y1760155867978891781"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        self.resp = self.session.post(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"tradeStatus":"SUCCESS"}
        assert result["tradeStatus"]==expect["tradeStatus"],self.msg.format(Except=expect["tradeStatus"],Really=result["tradeStatus"])
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()