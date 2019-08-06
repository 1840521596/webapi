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
class BearWord_Teacher_Test(unittest.TestCase):
    """<br>首页,教师端操作<br>
    1.admin-查询用户手机号<br>
    2.admin-添加用户手机号为教师<br>
    3.APP-个人中心-开启通知并判断是否教师角色<br>
    4.APP个人中心关闭接收作业<br>
    5.APP个人中心开启接收作业<br>
    6.admin-查询用户作业详情<br>
    7.admin-用户指定分配服务老师<br>
    8.admin-用户重新分配指定分配服务老师<br>
    9.老师端：待批改列表<br>
    10.老师端：用户作业详情<br>
    11.老师端：驳回理由列表<br>
    12.老师端：校验用户是否重新提交作业<br>
    13.老师端：上传批改语音接口<br>
    14.老师端：批改作业保存<br>
    15.老师端：批改记录<br>
    16.老师端：推荐/取消推荐优秀作业--推荐"""
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        self.env_flag = self.redis.str_get("wacc_mobile_env_flag")
        self.env_num = self.redis.str_get("wacc_mobile_env_num")
        self.timestamp = "%d"%(time.time())
        self.session = requests.Session()
        self.phone = self.redis.str_get("make_user_phones")
        header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
    def test_01_admin_bear_course_query_bearUser_list(self):
        """admin平台-运营管理-罐罐熊管理-添加罐罐熊老师-查询用户手机号<br>https://admin.yunshuxie.com/v1/bear_course/query/bearUser_list.json<br/>
        """
        cookies = get_wacc_admin_cookie(self.env_flag,self.env_num)
        url = r"https://admin.yunshuxie.com"+"/v1/bear_course/query/bearUser_list.json"
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        params = {"memberId":"","phone":self.phone,"sort":"memberId","order":"asc"}
        #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.get(url=url, params=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        if result["rows"]:
            bearWord_Teacher_memberId = result["rows"][0]["memberId"]
            self.redis.str_set("bearWord_Teacher_memberId",bearWord_Teacher_memberId,ex=60)
        else:
            print u"查询用户无数据"
            raise Exception,u"查询用户无数据"
    def test_02_admin_bear_course_add_bearTeacher(self):
        """admin平台-运营管理-罐罐熊管理-添加罐罐熊老师-添加用户手机号为老师<br>https://admin.yunshuxie.com/v1/bear_course/add_bearTeacher.htm<br/>
        """
        bearWord_Teacher_memberId = self.redis.str_get("bearWord_Teacher_memberId") if self.redis.str_get("bearWord_Teacher_memberId") else None
        if bearWord_Teacher_memberId:
            cookies = get_wacc_admin_cookie(self.env_flag,self.env_num)
            url = r"https://admin.yunshuxie.com"+"/v1/bear_course/add_bearTeacher.htm"
            header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "zh-CN,zh;q=0.9",
                      "Cache-Control": "no-cache", "Connection": "keep-alive",
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Origin": "https://admin.yunshuxie.com",
                      "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                      "X-Requested-With": "XMLHttpRequest"}
            params = {"memberId":bearWord_Teacher_memberId,"teacherType": "1"} #teacherType==2,测试老师
            #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = requests.get(url=url, params=params,headers=header,cookies=cookies)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.content + fengefu)
        else:
            print u"查询用户无数据"
            raise Exception,u"查询用户无数据"
    def test_03_v1_bear_main_personData(self):
        """App个人中心数据-是否开启通知和是否是老师<br>https://mobile.yunshuxie.com/v1/bear/main/personData.htm<br>"""
        url = r"https://mobile.yunshuxie.com" + r"/v1/bear/main/personData.htm"
        cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_04_v1_bear_teacher_bear_teacher(self):
        """罐罐熊-教师端-个人中心-接收作业开关-关闭<br>https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm<br>{"recieveStatus":"0"}"""
        url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm"
        params = {"recieveStatus":"0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie(self.env_flag,self.env_num,self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_05_v1_bear_teacher_bear_teacher(self):
        """罐罐熊-教师端-个人中心-接收作业开关-开启<br>https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm<br>{"recieveStatus":"1"}"""
        url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm"
        params = {"recieveStatus":"1"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie(self.env_flag,self.env_num,self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_06_admin_bear_course_query_bearMmeber_timeLine(self):
        """admin平台-查询用户详情<br>https://admin.yunshuxie.com/v1/bear_course/query/bearMmeber_timeLine.json"""
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/query/bearMmeber_timeLine.json"
        params ={"timeLineType":"8","phone":self.phone,"timeLineStatus": "6","beginDate": "","endDate":"","teacherPhone": "","order": "asc","limit": "10","offset": "0"}
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
        self.resp = requests.get(url=url,params=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        if result["rows"]:
            admin_workId = self.redis.str_set("admin_bearWord_workId", result["rows"][0]["timeLineId"],ex=60)
    def test_07_admin_bear_course_batch_job_assgin(self):
        """admin平台-分配指定服务老师<br>https://admin.yunshuxie.com/v1/bear_course/batch_job_assgin.htm"""
        workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/batch_job_assgin.htm"
        params ={"timelineIds": workId,"teacherPhone": self.phone,"assginJobStatus": "0"}
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
    def test_08_admin_bear_course_batch_job_assgin(self):
        """admin平台-重新分配指定服务老师<br>https://admin.yunshuxie.com/v1/bear_course/batch_job_assgin.htm"""
        workId = self.redis.str_get("admin_bearWord_workId") if self.redis.str_get("admin_bearWord_workId") else None
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/batch_job_assgin.htm"
        params ={"timelineIds": workId,"teacherPhone": self.phone,"assginJobStatus": "3"}
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
    def test_09_v1_bear_teacher_not_correct_list(self):
        """老师端：待批改列表<br>https://mobile.yunshuxie.com/v1/bear/teacher/not_correct_list.htm<br>{"page":"","pageSize":""}"""
        url =r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/not_correct_list.htm"
        params = {"page":"1","pageSize":"10"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        if result["data"]["notCorrectJobList"]:
            bearWord_timelineId = self.redis.str_set("bearWord_timelineId",result["data"]["notCorrectJobList"][0]["timelineId"])
        else:
            print u"当前教师未存在待批改作业"
            raise Exception,u"当前教师未存在待批改作业"
    def test_10_v1_bear_teacher_bear_task(self):
        """老师端：用户作业详情<br>https://mobile.yunshuxie.com/v1/bear/teacher/bear_task.htm<br>{"timeLineId":""}"""
        bearWord_timelineId = self.redis.str_get("bearWord_timelineId") if self.redis.str_get("bearWord_timelineId") else None
        if bearWord_timelineId:
            url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/bear_task.htm"
            params = {"timeLineId":bearWord_timelineId}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
            self.session.cookies = cookies
            self.resp = self.session.post(url=url, data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.content + fengefu)
            expect = {"returnCode": "0"}
            if result["returnCode"] == "0" or result["returnCode"] == 0:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
            if result["data"]:#["notCorrectJobList"]:
                # bearWord_timelineId = self.redis.str_set("bearWord_timelineId",
                #                                          result["data"]["notCorrectJobList"][0]["timelineId"])
                if result["data"]["submitUpdateDate"] !="":
                    bearWord_submitUpdateDate = self.redis.str_set("bearWord_submitUpdateDate",result["data"]["submitUpdateDate"])
        else:
            print u"当前教师未存在待批改作业"
            raise Exception,u"当前教师未存在待批改作业"
    def test_11_v1_bear_teacher_get_reject_reason_list(self):
        """驳回理由列表<br>https://mobile.yunshuxie.com/v1/bear/teacher/get_reject_reason_list.htm<br>"""
        url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/get_reject_reason_list.htm"
        cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
    def test_12_v1_bear_teacher_check_timeLineSatus(self):
        """老师端：校验用户是否重新提交作业<br>https://mobile.yunshuxie.com/v1/bear/teacher/check_timeLineSatus.htm<br>{"timeLineId":"","submitUpdateDate":""}"""
        bearWord_timelineId = self.redis.str_get("bearWord_timelineId") if self.redis.str_get("bearWord_timelineId") else None
        bearWord_submitUpdateDate = self.redis.str_get("bearWord_submitUpdateDate") if self.redis.str_get("bearWord_submitUpdateDate") else ""
        if bearWord_timelineId:
            url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/check_timeLineSatus.htm"
            cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
            params = {"timeLineId":bearWord_timelineId,"submitUpdateDate":bearWord_submitUpdateDate}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.session.cookies = cookies
            self.resp = self.session.post(url=url,data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.content + fengefu)
            expect = {"returnCode": "0"}
            if result["returnCode"] == "0" or result["returnCode"] == 0:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
        else:
            print u"当前教师未存在待批改作业"
            raise Exception, u"当前教师未存在待批改作业"
    def test_13_v1_bear_teacher_upload_voice(self):
        """上传批改语音接口<br>https://mobile.yunshuxie.com/v1/bear/teacher/upload_voice.htm<br>files=binary"""
        url = r"https://mobile.yunshuxie.com/v1/bear/teacher/upload_voice.htm"
        cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
        header = {"Connection": "keep-alive",  # "Content-Type": "multipart/form-data",
                  "User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        files = {
            'file': ("mp3.amr",open(r'./app/base/pythonProject/suite/wacc_mobile/mp3.amr', 'rb'),"multipart/form-data"),
        }
        str_params = """{'file': ("mp3.amr",open(r'mp3.amr', 'rb'),"multipart/form-data")}"""
        # logging.info(url + lianjiefu + str_params + fengefu)
        print str_params
        self.resp = requests.post(url=url,headers=header,files=files,cookies=cookies.get_dict())
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        if result["data"]["mp3"] != "":
            bearWord_mp3_link = self.redis.str_set("bearWord_mp3_link",result["data"]["mp3"],ex=60)
    def test_14_v1_bear_teacher_save_correction_records(self):
        """老师端：批改作业保存<br>https://mobile.yunshuxie.com/v1/bear/teacher/save_correction_records.htm<br>{"timeLineId":"","commentVoice":"","excellence":"","commentContent":""}"""
        bearWord_timelineId = self.redis.str_get("bearWord_timelineId") if self.redis.str_get("bearWord_timelineId") else None
        commentVoice = self.redis.str_get("bearWord_mp3_link") if self.redis.str_get("bearWord_mp3_link") else None
        bearWord_submitUpdateDate = self.redis.str_get("bearWord_submitUpdateDate") if self.redis.str_get("bearWord_submitUpdateDate") else ""
        if bearWord_timelineId and commentVoice:
            url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/check_timeLineSatus.htm"
            header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
                      "User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
            cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
            params = {"timeLineId":bearWord_timelineId,"excellence":"0","commentVoice":commentVoice,"commentContent":"测试批改保存","submitUpdateDate":bearWord_submitUpdateDate}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = requests.post(url=url,data=params,cookies=cookies,headers=header)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.content + fengefu)
            expect = {"returnCode": "0"}
            if result["returnCode"] == "0" or result["returnCode"] == 0:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
        else:
            print u"当前教师未存在待批改作业"
            raise Exception, u"当前教师未存在待批改作业"
    def test_15_v1_bear_teacher_corrected_record_list(self):
        """老师端：批改记录<br>https://mobile.yunshuxie.com/v1/bear/teacher/corrected_record_list.htm<br>{"page":"1","pageSize":"10","jobType":"0"}"""
        url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/corrected_record_list.htm"
        params = {"page":"1","pageSize":"10","jobType":"0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie(self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    # def test_16_v1_bear_teacher_recommend_job(self):
    #     """老师端：推荐/取消推荐优秀作业-推荐<br>https://mobile.yunshuxie.com/v1/bear/teacher/recommend_job.htm.htm<br>{"timeLineId":"","excellence":"1"}"""
    #     bearWord_timelineId = self.redis.str_get("bearWord_timelineId") if self.redis.str_get("bearWord_timelineId") else None
    #     if bearWord_timelineId:
    #         url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recommend_job.htm"
    #         params = {"timeLineId":bearWord_timelineId,"excellence":"1"}
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

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()