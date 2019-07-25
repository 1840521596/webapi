#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
#from app.base.pythonProject.base.getCookies import get_app_cookie
import time
logging = TestLog().getlog()
class BearWord_Test(unittest.TestCase):
    """<br>首页，不需要账号<br>1.首页，优秀作品墙，展示最新推荐的50份优秀作业。最多50份<br>2.首页，点击优秀作品墙的作品，可以打开作品详情页<br>3.首页，打开优秀作品详情页，可点击语音按钮播放老师的批改录音<br>4.首页，可给作品点赞或取消点赞<br>5.首页打开作品详情页，可分享到微信"""
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        env_flag = self.redis.str_get("wacc_moblie_env_flag")
        env_num = self.redis.str_get("wacc_mobile_env_num")
        self.timestamp = "%d"%(time.time())
        self.session = requests.Session()
        cookies = {"env_flag":env_flag,"env_num":env_num}  #get_app_cookie(env_flag,env_num) #未进行登录展示接口
        header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
    def test_00__app_release_version_get_app_version_v2(self):
        """APP获取更新提示<br>https://mobile.yunshuxie.com/v2/app_release_version/get_app_version_v2.htm<br/>
        """
        url = r"https://mobile.yunshuxie.com"+"/v2/app_release_version/get_app_version_v2.htm"
        params = {"appType":"bear_android","version":"1.0.1"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_01_bear_student_excellenceWorks(self):
        """APP，优秀作品墙，展示最新推荐的50份优秀作业。最多50份<br/>http://mobile.yunshuxie.com/v1/bear/student/excellenceWorks.htm<br/>{"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"2"}
        """
        url = r"http://mobile.yunshuxie.com"+"/v1/bear/student/excellenceWorks.htm"
        params = {"deviceId":"629a5eb2a857f86dadaa043b414984f2","version":"2"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode":"0"}
        if result["data"]:
            self.redis.str_set("bearWord_workId", result["data"][0]["workId"])
        else:
            self.redis.del_key("bearWord_workId")
        if result ["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
        assert len(result["data"])<=50,self.msg.format(Expect=u"最多50份",Really=u"大于50份")

    def test_02_bear_student_excellenceWorks(self):
        """微信，优秀作品墙，展示最新推荐的50份优秀作业。最多50份<br/>http://mobile.yunshuxie.com/v1/bear/student/excellenceWorks.htm<br/>{"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"2"}
        """
        url = r"http://mobile.yunshuxie.com"+"/v1/bear/student/excellenceWorks.htm"
        params = {"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"1"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode":"0"}
        if result ["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
        assert len(result["data"]) <= 50, self.msg.format(Expect=u"最多50份", Really=u"大于50份")
    def test_03_bear_main_index(self):
        """App首页轮播图和弹窗接口<br/>http://mobile.yunshuxie.com/v1/bear/main/index.htm<br/>{"version":"1"}
        """
        url = r"http://mobile.yunshuxie.com" + "/v1/bear/main/index.htm"
        params = {"version":"1"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"], Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
    def test_04_bear_student_workInfo(self):
        """作品展示详情<br/>http://mobile.yunshuxie.com/v1/bear/student/workInfo.htm<br/>{"workId":bearWord_workId,"deviceId":"629a5eb2a857f86dadaa043b414984f2"}"""
        bearWord_workId = self.redis.str_get("bearWord_workId")
        url = r"http://mobile.yunshuxie.com"+"/v1/bear/student/workInfo.htm"
        params = {"workId":bearWord_workId,"deviceId":"629a5eb2a857f86dadaa043b414984f2"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode":"0"}
        if result ["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
    def test_05_bear_student_praise(self):
        """点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/praise.htm<br/>{"workId":"1","deviceId":"1","isApp":"2"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId")
        url = r"http://mobile.yunshuxie.com"+"/v1/bear/student/praise.htm"
        params = {"workId":bearWord_workId,"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"2"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode":"0"}
        if result ["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
    def test_06_bear_student_praise(self):
        """点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/praise.htm<br/>{"workId":"1","deviceId":"1","isApp":"1"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId")
        url = r"http://mobile.yunshuxie.com"+"/v1/bear/student/praise.htm"
        params = {"workId":bearWord_workId,"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"1"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode":"0"}
        if result ["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
    def test_07_bear_student_cancelPraise(self):
        """取消点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/cancelPraise.htm<br/>{"workId":"1","deviceId":"1","isApp":"1"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId")
        url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/cancelPraise.htm"
        params = {"workId": bearWord_workId, "deviceId": "629a5eb2a857f86dadaa043b414984f2", "isApp": "1"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"], Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
    def test_08_bear_student_cancelPraise(self):
        """取消点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/cancelPraise.htm<br/>{"workId":"1","deviceId":"1","isApp":"2"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId")
        url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/cancelPraise.htm"
        params = {"workId": bearWord_workId, "deviceId": "629a5eb2a857f86dadaa043b414984f2", "isApp": "2"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"], Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                     Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()