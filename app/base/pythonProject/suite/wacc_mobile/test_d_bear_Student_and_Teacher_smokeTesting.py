#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_app_cookie,get_wacc_admin_cookie
import time
#logging = TestLog().getlog()
class BearWord_Student_and_Teacher_Test(unittest.TestCase):
    """<br>首页，账号登录<br>
    1.用户登录-我的作品展示列表<br>
    2.用户登录-我的作品展示列表&优秀作品&未点评&已点评<br>
    5.查询总结语列表<br>
    6.用户登录-评价老师接口（查看教师已点评的课程作品）（遍历进入课程，获取是否已分配服务老师）（找到存在服务老师的数据，进行评价）<br>
    7.教师登录：推荐/取消推荐优秀作业-取消推荐<br>
    8.教师登录：作业退回接口-教师端<br>
    9.教师登录：驳回接口-教师端
    """
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        self.env_flag = self.redis.str_get("wacc_mobile_env_flag")
        self.env_num = self.redis.str_get("wacc_mobile_env_num")
        self.timestamp = "%d" % (time.time())
        self.session = requests.Session()
        cookies = {"env_flag": self.env_flag,
                   "env_num": self.env_num}  # get_app_cookie(self.env_flag,self.env_num) #未进行登录展示接口
        self.header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
                       "User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = self.header
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.phone = self.redis.str_get("make_user_phones")
    def test_01_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"4"全部作品,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "4", "page": "1"}
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, data=params, cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_02_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"3"优秀作品,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "3", "page": "1"}
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_03_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"2"未点评,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "2", "page": "1"}
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_04_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"1"已点评,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "1", "page": "1"}
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_05_bear_student_summary(self):
        """用户登录-查询总结语列表<br>http://mobile.yunshuxie.com/v1/bear/student/summary.htm<br/>"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
        params = {"type": "4"}
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_06_admin_bear_course_query_bearMmeber_timeLine(self):
        """admin平台-查询用户详情<br>https://admin.yunshuxie.com/v1/bear_course/query/bearMmeber_timeLine.json"""
        url = r"https://admin.yunshuxie.com" + r"/v1/bear_course/query/bearMmeber_timeLine.json"
        params = {"timeLineType": "8", "phone": self.phone, "timeLineStatus": "6", "beginDate": "", "endDate": "",
                  "teacherPhone": "", "order": "asc", "limit": "10", "offset": "0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_wacc_admin_cookie(self.env_flag, self.env_num)
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        self.resp = requests.get(url=url, params=params, headers=header, cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        admin_workId = self.redis.str_set("admin_bearWord_workId", result["rows"][0]["timeLineId"])
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/batch_job_assgin.htm"
        params ={"timelineIds": admin_workId,"teacherPhone": self.phone,"assginJobStatus": "0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_wacc_admin_cookie(self.env_flag, self.env_num)
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        self.resp = requests.post(url=url,data=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
    # def test_06_v1_bear_teacher_save_correction_records(self):
    #     """老师端：批改作业保存<br>https://mobile.yunshuxie.com/v1/bear/teacher/save_correction_records.htm<br>{"timeLineId":"","commentVoice":"","excellence":"","commentContent":""}"""
    #     bearWord_timelineId = self.redis.str_get("bearWord_timelineId") if self.redis.str_get(
    #         "bearWord_timelineId") else None
    #     commentVoice = self.redis.str_get("bearWord_mp3_link") if self.redis.str_get("bearWord_mp3_link") else None
    #     bearWord_submitUpdateDate = self.redis.str_get("bearWord_submitUpdateDate") if self.redis.str_get(
    #         "bearWord_submitUpdateDate") else ""
    #     if bearWord_timelineId and commentVoice:
    #         url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/check_timeLineSatus.htm"
    #         cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
    #         params = {"timeLineId": bearWord_timelineId, "excellence": "0", "commentVoice": commentVoice,
    #                   "commentContent": "测试批改保存", "submitUpdateDate": bearWord_submitUpdateDate}
    #         # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
    #         str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
    #         print str_params
    #         self.session.cookies = cookies
    #         self.resp = self.session.post(url=url, data=params)
    #         print self.resp.text
    #         result = json.loads(self.resp.text, encoding="utf8")
    #         # logging.info(url + lianjiefu + self.resp.content + fengefu)
    #         expect = {"returnCode": "0"}
    #         if result["returnCode"] == "0" or result["returnCode"] == 0:
    #             assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                  Really=result["returnCode"])
    #         else:
    #             assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                  Really=result["returnCode"])
    #     else:
    #         print u"当前教师未存在待批改作业"
    #         raise Exception, u"当前教师未存在待批改作业"
    # def test_07_bear_student_commentTeacher(self):
    #     """用户登录-评价老师接口<br>http://mobile.yunshuxie.com/v1/bear/student/commentTeacher.htm<br/>"""
    #     url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
    #     params = {"type": "1", "page": "1"}  # 查看教师已点评的课程作品
    #     cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
    #     # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
    #     self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
    #     result = json.loads(self.resp.text, encoding="utf8")
    #     # logging.info(url + lianjiefu + self.resp.text + fengefu)
    #     workId_list = []
    #     if result["data"]["list"]:
    #         for m in result["data"]["list"]:
    #             workId_list.append(m["workId"])
    #         # 查看课程作品，判断是否存在teacherId
    #         for workId in workId_list:
    #             url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/workInfo.htm"
    #             params = {"workId": workId, "deviceId": "629a5eb2a857f86dadaa043b414984f2"}
    #             # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
    #             str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
    #             self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
    #             result = json.loads(self.resp.text, encoding="utf8")
    #             # logging.info(url + lianjiefu + self.resp.text + fengefu)
    #             if result["data"]["teacherId"] != "":
    #                 workId = result["data"]["workId"]
    #                 teacherId = result["data"]["teacherId"]
    #                 break
    #             else:
    #                 print u"未存在已点评已分配教师的作品数据"
    #                 raise Exception, u"未存在已点评已分配教师的作品数据"
    #         url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/commentTeacher.htm"
    #         params = {"workId": workId, "teacherId": teacherId, "commentContent": "测试评价教师功能", "commentStar": "5",
    #                   "isApp": "2"}
    #         cookies = get_app_cookie(self.env_flag, self.env_num, phone=self.phone)
    #         self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
    #         print self.resp.text
    #         result = json.loads(self.resp.text, encoding="utf8")
    #         # logging.info(url + lianjiefu + self.resp.text + fengefu)
    #         expect = {"returnCode": "0"}
    #         if result["returnCode"] == "0" or result["returnCode"] == 0:
    #             assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                  Really=result["returnCode"])
    #         else:
    #             assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                  Really=result["returnCode"])
    #     else:
    #         print u"未存在教师已点评的课程作品数据"
    #         raise Exception, u"未存在教师已点评的课程作品数据"


    # def test_07_v1_bear_teacher_recommend_job(self):
    #     """老师端：推荐/取消推荐优秀作业-取消推荐<br>https://mobile.yunshuxie.com/v1/bear/teacher/recommend_job.htm.htm<br>{"timeLineId":"","excellence":"0"}"""
    #     bearWord_timelineId = self.redis.str_get("bearWord_timelineId") if self.redis.str_get("bearWord_timelineId") else None
    #     if bearWord_timelineId:
    #         url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recommend_job.htm"
    #         params = {"timeLineId":bearWord_timelineId,"excellence":"0"}
    #         # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
    #         str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
    #         print str_params
    #         cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
    #         self.session.cookies = cookies
    #         self.resp = self.session.post(url=url,data=params)
    #         print self.resp.text
    #         result = json.loads(self.resp.text, encoding="utf8")
    #         #logging.info(url + lianjiefu + self.resp.content + fengefu)
    #         expect = {"returnCode": "0"}
    #         if result["returnCode"] == "0" or result["returnCode"] == 0:
    #             assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                  Really=result["returnCode"])
    #         else:
    #             assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                  Really=result["returnCode"])
    #     else:
    #         print u"当前教师未存在待批改作业"
    #         raise Exception,u"当前教师未存在待批改作业"
    # def test_08_bear_teacher_reject_job(self):
    #     """作业退回接口-教师端<br>https://mobile.yunshuxie.com/v1/bear/teacher/return_job.htm<br/>{"timeLineId":""}"""
    #     if self.env_flag != "beta":
    #         print u"当前运行环境非beta,跳过打卡接口"
    #     else:
    #         workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
    #         if workId:
    #             url = r"http://mobile.yunshuxie.com" + "/v1/bear/teacher/return_job.htm"
    #             params = {"timeLineId":workId}
    #             #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
    #             str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
    #             print str_params
    #             self.resp = self.session.post(url=url, data=params)
    #             print self.resp.text
    #             result = json.loads(self.resp.text, encoding="utf8")
    #             #logging.info(url + lianjiefu + self.resp.text + fengefu)
    #             expect = {"returnCode": "0"}
    #             if result["returnCode"] == "0" or result["returnCode"] == 0:
    #                 assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                      Really=result["returnCode"])
    #             else:
    #                 assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                      Really=result["returnCode"])
    #         else:
    #             print u"当前页面不存在章节数据"
    #             raise Exception, u"当前页面不存在章节数据"
    # def test_09_bear_teacher_reject_job(self):
    #     """ 驳回接口-教师端<br>https://mobile.yunshuxie.com/v1/bear/teacher/reject_job.htm<br/>{"timeLineId":"","reasonId":"","status":""}"""
    #     if self.env_flag != "beta":
    #         print u"当前运行环境非beta,跳过打卡接口"
    #     else:
    #         workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
    #         if workId:
    #             url = r"http://mobile.yunshuxie.com" + "/v1/bear/teacher/reject_job.htm"
    #             params = {"timeLineId":workId,"reasonId":"1","status":"1"}
    #             #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
    #             str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
    #             print str_params
    #             self.resp = self.session.post(url=url, data=params)
    #             print self.resp.text
    #             result = json.loads(self.resp.text, encoding="utf8")
    #             #logging.info(url + lianjiefu + self.resp.text + fengefu)
    #             expect = {"returnCode": "0"}
    #             if result["returnCode"] == "0" or result["returnCode"] == 0:
    #                 assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                      Really=result["returnCode"])
    #             else:
    #                 assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
    #                                                                                      Really=result["returnCode"])
    #         else:
    #             print u"当前页面不存在章节数据"
    #             raise Exception, u"当前页面不存在章节数据"

    @classmethod
    def tearDownClass(self):
        pass
