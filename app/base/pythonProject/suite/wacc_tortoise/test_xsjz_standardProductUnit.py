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
globals_values = {}
class StandardProductUnit_Test(unittest.TestCase):
    """销售简章-SPU相关操作协议"""
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
    def test_01_spu_save(self):
        """添加spu接口协议<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":112,"title":"测试商品",<br/>"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"测试"","shareInfo":"测试","coupon":0,"introduceImgs":"测试使用","pcImgs":"测试","introduce":"测试"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/save.htm"
        timestamp = "%d"%(time.time())
        params = {"type":112,"title":"测试商品-title-%s"%(timestamp),"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",
                  "sellerPoint":"测试-sellerPoint-%s"%(timestamp),"shareInfo":"测试-shareInfo-%s"%(timestamp),"coupon":0,"introduceImgs":"测试使用-introduceImgs-%s" % (timestamp),
                  "pcImgs":"测试","introduce":"测试%s"%(timestamp)}
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
        globals()["globals_values"]["spu_id"] = result["data"]["id"]
    def test_02_spu_save(self):
        """添加spu接口协议-选填项为空<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":112,"title":"测试商品",<br/>"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"","shareInfo":"","coupon":0,"introduceImgs":"测试使用","pcImgs":"","introduce":"测试使用-introduceImgs"}
        """
        url = r"http://adm.yunshuxie.com" + "/api/spu/save.htm"
        timestamp = "%d" % (time.time())
        params = {"type": 112, "title": "测试商品-title-%s" % (timestamp),
                  "imgUrls": "https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",
                  "sellerPoint": "", "shareInfo": "",
                  "coupon": 0, "introduceImgs": "测试使用-introduceImgs-%s" % (timestamp),
                  "pcImgs": "", "introduce": "测试使用-introduceImgs-%s" % (timestamp)}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
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
    def test_03_spu_save(self):
        """添加SPU接口协议-imgUrls&introduceImgs&pcImgs<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":112,"title":"测试商品","imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"测试","shareInfo":"测试","coupon":0,"introduceImgs":"测试使用",<br/>"pcImgs":"测试","introduce":"测试"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/save.htm"
        timestamp = "%d"%(time.time())
        params = {"type":112,"title":"测试商品-title-%s"%(timestamp),
                  "imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg,https://oss-ysx-pic.yunshuxie.com/agent_c/2018/12/15/00/1544803384770.png",
                  "sellerPoint":"测试-sellerPoint-%s"%(timestamp),"shareInfo":"测试-shareInfo-%s"%(timestamp),"coupon":0,
                  "introduceImgs":"测试使用-introduceImgs-%s"%(timestamp),"pcImgs":"测试-pcImgs-%s"%(timestamp),"introduce":"测试-introduce-%s"%(timestamp)}
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
        globals()["globals_values"]["spu_id"] = result["data"]["id"]
    def test_04_spu_getList(self):
        """获取spu列表信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getList.htm<br/>{"pageIndex":1,"pageSize":10,"title":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/getList.htm"
        params = {"pageIndex":1,"pageSize":10,"title":""}
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
    def test_05_spu_getRow(self):
        """获取单条spu信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getRow.htm<br/>{"id":}"""
        url = r"http://adm.yunshuxie.com"+"/api/spu/getRow.htm"
        params = {"id":globals_values["spu_id"]}
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
    def test_06_spu_update(self):
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

    def test_07_spu_getInfo(self):
        """获取单条spu以及相关sku信息接口协议-SPU不存在<br/>http://adm.yunshuxie.com/api/spu/getInfo.htm<br/>{"id":1}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/getInfo.htm"
        params = {"id":1}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"10002"}
        if result ["code"] == "10002" or result["code"] == 10002:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_08_spu_getInfo(self):
        """获取单条spu以及相关sku信息接口协议-childList=[]<br/>http://adm.yunshuxie.com/api/spu/getInfo.htm<br/>{"id":}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/getInfo.htm"
        spu_id = int(globals_values["spu_id"])
        params = {"id":spu_id}
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
    def test_09_spu_getInfo(self):
        """获取单条spu以及相关sku信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getInfo.htm<br/>{"id":2}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/getInfo.htm"
        params = {"id": 2}
        self.resp = self.session.post(url=url,params=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_10_spu_delete(self):
        """删除单条spu信息接口协议<br/>http://adm.yunshuxie.com/api/spu/delete.htm<br/>{"id":}
        """
        url = r"http://adm.yunshuxie.com"+"/api/spu/delete.htm"
        params = {"id":globals_values["spu_id"]}
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
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()