#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_xsjz_cookie
import time
logging = TestLog().getlog()
timestamp = "%d"%(time.time())
globals_values = {}
class Smoke_Testing(unittest.TestCase):
    """销售简章-添加类目相关协议-添加SPU-添加SKU"""
    @classmethod
    def setUpClass(self):
        redis = MyRedis()
        env_flag = redis.str_get("wacc_tortoise_env_flag")
        env_num = redis.str_get("wacc_tortoise_env_num")
        self.session = requests.Session()
        cookies = get_xsjz_cookie(env_flag,env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*","Connection":"keep-alive"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_00_productType_getTreeList(self):
        """商品类型树形结构接口协议<br/>http://adm.yunshuxie.com/api/productType/getTreeList.htm
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getTreeList.htm"
        self.resp = self.session.post(url=url)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_01_productType_save(self):
        """添加类目接口协议<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"自动化测试-pTitle-","pId":"","childTitle":"自动化测试-childTitle-"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"自动化测试-pTitle-{timestamp}".format(timestamp=timestamp),"pId":"","childTitle":"自动化测试-childTitle-{timestamp}".format(timestamp=timestamp)}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
        globals()["globals_values"]["pTitle"] = params["pTitle"]
    def test_02_productType_getList(self):
        """获取单条类目首级节点对应信息接口协议<br/>title=<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":1,"pageSize":2,"title":}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getList.htm"
        params = {"pageIndex":0,"pageSize":2,"title":globals_values["pTitle"]}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
        globals()["globals_values"]["id"] = result["data"]["list"][0]["id"]
    def test_03_productType_getRow(self):
        """获取单条类目首级节点对应信息接口协议<br/>http://adm.yunshuxie.com/api/productType/getRow.htm<br/>{"id":}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getRow.htm"
        params = {"id":globals_values["id"]}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_04_productType_update(self):
        """获取单条类目首级节点对应信息接口协议<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id":,"title":}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/update.htm"
        params = {"id":globals_values["id"],"title":globals_values["pTitle"]}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False,encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_05_spu_save(self):
        """添加spu接口协议<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":,"title":"自动化测试",<br/>"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"自动化测试"","shareInfo":"自动化测试","coupon":0,"introduceImgs":"自动化测试","pcImgs":"自动化测试","introduce":"自动化测试"}
        """
        url = r"http://adm.yunshuxie.com" + "/api/spu/save.htm"  #暂时使用Mock 数据
        #url = r"http://uwsgi.sys.bandubanxie.com/mock" + "/api/spu/save.htm"
        timestamp = "%d" % (time.time())
        params = {"type": globals_values["id"], "title": "测试商品-title-%s" % (timestamp),
                  "imgUrls": "https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",
                  "sellerPoint": "测试-sellerPoint-%s" % (timestamp), "shareInfo": "测试-shareInfo-%s" % (timestamp),
                  "coupon": 0, "introduceImgs": "测试使用-introduceImgs-%s" % (timestamp),
                  "pcImgs": "测试", "introduce": "测试%s" % (timestamp)}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"code": "0"}
        if result["code"] == "0" or result["code"] == 0:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
        globals()["globals_values"]["spu_title"] = params["title"]
    def test_06_spu_getList(self):
        """获取spu列表信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getList.htm<br/>{"pageIndex":1,"pageSize":10,"title":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/getList.htm"
        #url = r"http://uwsgi.sys.bandubanxie.com/mock"+"/api/spu/getList.htm"
        params = {"pageIndex":1,"pageSize":10,"title":globals_values["spu_title"]}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False,encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
        globals()["globals_values"]["spu_id"] = result["data"][0]["id"]
    def test_07_spu_getRow(self):
        """获取单条spu信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getRow.htm<br/>{"id":}"""
        url = r"http://adm.yunshuxie.com"+"/api/spu/getRow.htm"
        params = {"id":globals_values["spu_id"]}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False,encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                    Really=result["code"])
    def test_08_spu_update(self):
        """更新spu接口协议<br/>http://adm.yunshuxie.com/api/spu/update.htm<br/>{"id":}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/update.htm"
        timestamp = "%d" % (time.time())
        params = {"id":globals_values["spu_id"],"title":"测试使用-title-%s"%timestamp,
                  "imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "sellerPoint":"测试-sellerPoint-%s"%timestamp,"shareInfo":"测试-shareInfo-%s"%timestamp,"coupon":1,
                  "introduceImgs":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "pcImgs":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "introduce":"测试使用-introduce-%s"%timestamp}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False,encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()