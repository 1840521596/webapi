#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_app_cookie,get_wacc_admin_cookie
import time
logging = TestLog().getlog()
class BearWord_Student_Test(unittest.TestCase):
    """<br>首页，不需要账号<br>1.获取版本更新提示,进入首页<br>2.APP展示最新推荐的并最多50份优秀作业<br>3.微信展示最新推荐的并最多50份优秀作业<br>4.App首页轮播图和弹窗接口<br>5.优秀作品墙作品展示详情<br>6.APP点赞接口<br>7.微信点赞接口<br>8.微信取消点赞接口<br>9.APP取消点赞接口<br>10.首页打开作品详情页，可分享到微信<br>11.我的作品查看-全部作品&优秀作品&未点评&已点评<br>12.查询总结语列表<br>13.学生评价教师接口（查看教师已点评的课程作品）（遍历进入课程，获取是否已分配服务老师）（找到存在服务老师的数据，进行评价）"""
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        self.env_flag = self.redis.str_get("wacc_moblie_env_flag")
        self.env_num = self.redis.str_get("wacc_mobile_env_num")
        self.timestamp = "%d"%(time.time())
        self.session = requests.Session()
        cookies = {"env_flag":self.env_flag,"env_num":self.env_num}#get_app_cookie(self.env_flag,self.env_num) #未进行登录展示接口
        self.header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = self.header
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.phone = self.redis.str_get("make_user_phones")
    def test_00_admin_v1_elementary_joinCategoryProduct(self):
        """罐罐熊练字课-用户授权课程<br>https://admin.yunshuxie.com/v1/elementary/joinCategoryProduct.json"""
        cookies = get_wacc_admin_cookie(self.env_flag,self.env_num)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        url = r"https://admin.yunshuxie.com"+r"/v1/admin/edit_book/query/AllVipmember_list.json"  #查询授权手机号
        params = {"memberId":"","memberPhone":self.phone,"sort":"memberId","order":"desc","limit":"10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.get(url=url,headers=headers,cookies=cookies,params=params)
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        if result["rows"]:
            memberId = result["rows"][0]["memberId"]
            url = r"https://admin.yunshuxie.com"+r"/v1/elementary/query/category_elementary_course_list.json"
            params = {"memberId":"","categoryId":"102","sort":"productId","order":"desc","limit":"10","offset":"0"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = requests.get(url=url, headers=headers, cookies=cookies, params=params)
            result = json.loads(self.resp.text, encoding="utf8")
            logging.info(url + lianjiefu + self.resp.content + fengefu)
            url = r"https://admin.yunshuxie.com"+r"/v1/elementary/joinCategoryProduct.json"
            if result["rows"]:
                for datas in result["rows"]:
                    productCoursehourseId = datas["productCoursehourseId"]
                    params = {"memberId":memberId,"productCoursehourseId":productCoursehourseId,
                              "orderId":"","accreditReason":"测试","phone":self.phone,"categoryId":"102","orderSn":""}
                    self.resp = requests.post(url=url, headers=headers, cookies=cookies, params=params)
                    logging.info(url + lianjiefu + self.resp.content + fengefu)
                    result = json.loads(self.resp.text, encoding="utf8")
                    if result["returnCode"] == "0" or result["returnCode"] == 0:
                        print u"phone:%s添加课程期次%s成功"%(self.phone,productCoursehourseId)
                    else:
                        print u"phone:%s用户添加课程期次%s失败%s"%(self.phone,productCoursehourseId)
                        raise Exception,u"phone:%s用户添加课程期次%s失败%s"%(self.phone,productCoursehourseId)
            else:
                print u"不存在课程期次"
                raise Exception,u"不存在课程期次"
        else:
            print u"用户不存在"
            raise Exception,u"用户不存在"
    def test_01_app_release_version_get_app_version_v2(self):
        """用户未登录-APP获取更新提示<br>https://mobile.yunshuxie.com/v2/app_release_version/get_app_version_v2.htm<br/>
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
    def test_02_bear_student_excellenceWorks(self):
        """用户未登录-APP，优秀作品墙，展示最新推荐的50份优秀作业。最多50份<br/>http://mobile.yunshuxie.com/v1/bear/student/excellenceWorks.htm<br/>{"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"2"}
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
    def test_03_bear_student_excellenceWorks(self):
        """用户未登录-微信，优秀作品墙，展示最新推荐的50份优秀作业。最多50份<br/>http://mobile.yunshuxie.com/v1/bear/student/excellenceWorks.htm<br/>{"deviceId":"629a5eb2a857f86dadaa043b414984f2","isApp":"2"}
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
    def test_04_bear_main_index(self):
        """用户未登录-App首页轮播图和弹窗接口<br/>http://mobile.yunshuxie.com/v1/bear/main/index.htm<br/>{"version":"1"}
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
    def test_05_bear_student_workInfo(self):
        """用户未登录-作品展示详情<br/>http://mobile.yunshuxie.com/v1/bear/student/workInfo.htm<br/>{"workId":bearWord_workId,"deviceId":"629a5eb2a857f86dadaa043b414984f2"}"""
        bearWord_workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
        if bearWord_workId:
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
        else:
            print u"未存在作品展示"
            raise Exception,u"未存在作品展示"
    def test_06_bear_student_praise(self):
        """用户未登录-点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/praise.htm<br/>{"workId":"1","deviceId":"1","isApp":"2"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
        if bearWord_workId:
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
        else:
            print u"未存在作品展示"
    def test_07_bear_student_praise(self):
        """用户未登录-点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/praise.htm<br/>{"workId":"1","deviceId":"1","isApp":"1"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
        if bearWord_workId:
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
        else:
            print u"未存在作品展示"
    def test_08_bear_student_cancelPraise(self):
        """用户未登录-取消点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/cancelPraise.htm<br/>{"workId":"1","deviceId":"1","isApp":"1"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
        if bearWord_workId:
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
        else:
            print u"取消点赞接口未存在数据"
    def test_09_bear_student_cancelPraise(self):
        """用户未登录-取消点赞接口<br/>http://mobile.yunshuxie.com/v1/bear/student/cancelPraise.htm<br/>{"workId":"1","deviceId":"1","isApp":"2"}
        """
        bearWord_workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
        if bearWord_workId:
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
        else:
            print u"取消点赞接口未存在数据"
    def test_10_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"4"全部作品,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com"+r"/v1/bear/student/myWorkList.htm"
        params = {"type":"4","page":"1"}
        cookies = get_app_cookie(self.env_flag,self.env_num,phone=self.phone)
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url,headers=self.header,data=params,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_11_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"3"优秀作品,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com"+r"/v1/bear/student/myWorkList.htm"
        params = {"type":"3","page":"1"}
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_12_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"2"未点评,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com"+r"/v1/bear/student/myWorkList.htm"
        params = {"type":"2","page":"1"}
        cookies = get_app_cookie(self.env_flag,self.env_num,phone=self.phone)
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_13_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"1"已点评,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com"+r"/v1/bear/student/myWorkList.htm"
        params = {"type":"1","page":"1"}
        cookies = get_app_cookie(self.env_flag,self.env_num,phone=self.phone)
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_14_bear_student_summary(self):
        """用户登录-查询总结语列表<br>http://mobile.yunshuxie.com/v1/bear/student/summary.htm<br/>"""
        url = r"http://mobile.yunshuxie.com"+r"/v1/bear/student/myWorkList.htm"
        cookies = get_app_cookie(self.env_flag,self.env_num,phone=self.phone)
        params = {"type":"4"}
        self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_15_bear_student_commentTeacher(self):
        """用户登录-评价老师接口<br>http://mobile.yunshuxie.com/v1/bear/student/commentTeacher.htm<br/>"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "1", "page": "1"}  #查看教师已点评的课程作品
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        workId_list = []
        if result["data"]["list"]:
            for m in result["data"]["list"]:
                workId_list.append(m["workId"])
        #查看课程作品，判断是否存在teacherId
            for workId in workId_list:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/workInfo.htm"
                params = {"workId": workId, "deviceId": "629a5eb2a857f86dadaa043b414984f2"}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
                result = json.loads(self.resp.text, encoding="utf8")
                logging.info(url + lianjiefu + self.resp.text + fengefu)
                if result["data"]["teacherId"] != "":
                    workId = result["data"]["workId"]
                    teacherId = result["data"]["teacherId"]
                    break
                else:
                    print u"未存在已点评已分配教师的作品数据"
                    raise Exception,u"未存在已点评已分配教师的作品数据"
            url = r"http://mobile.yunshuxie.com"+r"/v1/bear/student/commentTeacher.htm"
            params = {"workId":workId,"teacherId":teacherId,"commentContent":"测试评价教师功能","commentStar":"5","isApp":"1"}
            self.resp = requests.post(url=url,headers=self.header,cookies=cookies,data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            logging.info(url + lianjiefu + self.resp.text + fengefu)
            expect = {"returnCode": "0"}
            if result["returnCode"] == "0" or result["returnCode"] == 0:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
        else:
            print u"未存在教师已点评的课程作品数据"
            raise Exception,u"未存在教师已点评的课程作品数据"
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()