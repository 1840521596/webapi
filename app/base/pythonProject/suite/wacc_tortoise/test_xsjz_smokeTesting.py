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
class Smoke_Testing(unittest.TestCase):
    """销售简章-添加类目相关协议-添加SPU-添加SKU"""
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        env_flag = self.redis.str_get("wacc_tortoise_env_flag")
        env_num = self.redis.str_get("wacc_tortoise_env_num")
        self.timestamp = "%d" % (time.time())
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
        """添加类目接口协议<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"冒烟自动化测试-pTitle-","pId":"","childTitle":"冒烟自动化测试-childTitle-"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"冒烟自动化测试-pTitle-{timestamp}".format(timestamp=self.timestamp),
                  "pId":"","childTitle":"冒烟自动化测试-childTitle-{timestamp}".format(timestamp=self.timestamp)}
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
        self.redis.str_set("pTitle",params["pTitle"])
    def test_02_productType_getList(self):
        """获取单条类目首级节点对应信息接口协议<br/>title=<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":1,"pageSize":2,"title":}
        """
        pTitle = self.redis.str_get("pTitle")
        url = r"http://adm.yunshuxie.com"+"/api/productType/getList.htm"
        params = {"pageIndex":0,"pageSize":2,"title":pTitle}
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
        self.redis.str_set("product_id",result["data"]["list"][0]["id"])
    def test_03_productType_getRow(self):
        """获取单条类目首级节点对应信息接口协议<br/>http://adm.yunshuxie.com/api/productType/getRow.htm<br/>{"id":}
        """
        productId = self.redis.str_get("product_id")
        url = r"http://adm.yunshuxie.com"+"/api/productType/getRow.htm"
        params = {"id":productId}
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
        productId = self.redis.str_get("product_id")
        pTitle = self.redis.str_get("pTitle")
        url = r"http://adm.yunshuxie.com"+"/api/productType/update.htm"
        params = {"id":productId,"title":pTitle}
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
        """添加spu接口协议<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":,"title":"冒烟自动化测试",<br/>"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"冒烟自动化测试"","shareInfo":"冒烟自动化测试","coupon":0,"introduceImgs":"冒烟自动化测试","pcImgs":"冒烟自动化测试","introduce":"冒烟自动化测试"}
        """
        productId = self.redis.str_get("product_id")
        url = r"http://adm.yunshuxie.com" + "/api/spu/save.htm"  #暂时使用Mock 数据
        #url = r"http://uwsgi.sys.bandubanxie.com/mock" + "/api/spu/save.htm"
        params = {"type": productId, "title": "冒烟自动化测试商品-title-%s" % (self.timestamp),
                  "imgUrls": "https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",
                  "sellerPoint": "冒烟自动化测试-sellerPoint-%s" % (self.timestamp),
                  "shareInfo": "冒烟自动化测试-shareInfo-%s" % (self.timestamp),
                  "coupon": 0, "introduceImgs": "冒烟自动化测试-introduceImgs-%s" % (self.timestamp),
                  "pcImgs": "冒烟自动化测试", "introduce": "冒烟自动化测试%s" % (self.timestamp)}
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
        self.redis.str_set("spu_title",params["title"])
    def test_06_spu_getList(self):
        """获取spu列表信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getList.htm<br/>{"pageIndex":1,"pageSize":10,"title":""}
        """
        spu_title = self.redis.str_get("spu_title")
        url = r"http://adm.yunshuxie.com"+"/api/spu/getList.htm"
        #url = r"http://uwsgi.sys.bandubanxie.com/mock"+"/api/spu/getList.htm"
        params = {"pageIndex":0,"pageSize":10,"title":spu_title}
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
        self.redis.str_set("spu_id",result["data"]["list"][0]["id"])
    def test_07_spu_getRow(self):
        """获取单条spu信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getRow.htm<br/>{"id":}"""
        url = r"http://adm.yunshuxie.com"+"/api/spu/getRow.htm"
        spu_id = self.redis.str_get("spu_id")
        params = {"id":spu_id}
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
        spu_id = self.redis.str_get("spu_id")
        url = r"http://adm.yunshuxie.com"+"/api/spu/update.htm"
        params = {"id":spu_id,"title":"冒烟自动化测试-title-%s"%self.timestamp,
                  "imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "sellerPoint":"冒烟自动化测试-sellerPoint-%s"%self.timestamp,
                  "shareInfo":"冒烟自动化测试-shareInfo-%s"%self.timestamp,"coupon":1,
                  "introduceImgs":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "pcImgs":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "introduce":"冒烟自动化测试-introduce-%s"%self.timestamp}
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
    def test_09_sku_save(self):
        """添加sku接口协议<br/>"""
        spu_id = self.redis.str_get("spu_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/save.htm"
        params = {"spuId":spu_id,"attributeIds":"123","marketPrice":"999","shopPrice":"999","courseIds":"","stocks":""}
    @classmethod
    def tearDownClass(self):
        pass
if __name__ == "__main__":
    unittest.main()