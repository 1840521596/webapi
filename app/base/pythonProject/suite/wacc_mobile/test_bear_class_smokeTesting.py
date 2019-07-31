#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_app_cookie
import time
logging = TestLog().getlog()
class BearWord_Class_Test(unittest.TestCase):
    """<br>学生端-上课<br>1.未登录，上课页显示登录按钮<br>2.已登录（微信）<br>3.已登录-存在课程（APP）4.章节列表接口<br>5.视频播放到70%即为已学习状态，解锁上传作品按钮<br>6.上传作业，成功上传<br>7.打卡接口<br>8.作业被点评前，重新上传作业成功<br>9.教师端-作业退回接口<br>10.教师端-作业驳回接口"""
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        self.env_flag = self.redis.str_get("wacc_mobile_env_flag")
        self.env_num = self.redis.str_get("wacc_mobile_env_num")
        self.timestamp = "%d"%(time.time())
        self.session = requests.Session()
        self.header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = self.header
        self.phone_Exist_Course = "60000009092"  #存在课程
    def test_01_bear_student_courseList(self):
        """课程列表接口-未登录<br>https://mobile.yunshuxie.com/v1/bear/student/courseList.htm<br/>{"page":"1","isApp":"2"}
        """
        url = r"https://mobile.yunshuxie.com"+"/v1/bear/student/courseList.htm"
        params = {"page":"1","isApp":"2"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        cookies = {"env_flag":self.env_flag,"env_num":self.env_num}
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "4"}
        if result["returnCode"] == "4" or result["returnCode"] == 4:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_02_bear_student_courseList(self):
        """课程列表接口-已登录<br>https://mobile.yunshuxie.com/v1/bear/student/courseList.htm<br/>{"page":"1","isApp":"1"}
        """
        cookies = get_app_cookie(self.env_flag,self.env_num) #进行登录展示接口_新用户
        self.session.cookies = cookies
        url = r"https://mobile.yunshuxie.com"+"/v1/bear/student/courseList.htm"
        params = {"page":"1","isApp":"1"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
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
    def test_03_bear_student_courseList(self):
        """课程列表接口-已登录(存在课程)<br>https://mobile.yunshuxie.com/v1/bear/student/courseList.htm<br/>{"page":"1","isApp":"1"}"""
        cookies = get_app_cookie(self.env_flag,self.env_num,phone=self.phone_Exist_Course) #进行登录展示接口_新用户
        self.session.cookies = cookies
        url = r"https://mobile.yunshuxie.com" + "/v1/bear/student/courseList.htm"
        params = {"page": "1", "isApp": "2"}
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
        if result["data"]["list"]:
            productCourseId = self.redis.str_set("bearWord_productCourseId",result["data"]["list"][0]["productCourseId"])
        else:
            self.redis.del_key("bearWord_productCourseId")  #删除历史key数据
    def test_04_bear_student_chapterList(self):
        """ 章节列表接口<br>https://mobile.yunshuxie.com/v1/bear/student/chapterList.htm<br/>{"productCourseId":"","isApp":"2"}"""
        productCourseId = self.redis.str_get("bearWord_productCourseId") if self.redis.str_get("bearWord_productCourseId") else None
        if productCourseId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/chapterList.htm"
            params = {"productCourseId":productCourseId,"isApp":"2"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = self.session.post(url=url, data=params)
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
            if result["data"]["list"]:
                productChapterId = self.redis.str_set("bearWord_productChapterId",result["data"]["list"][0]["productChapterId"])
            else:
                self.redis.del_key("bearWord_productChapterId")
        else:
            print u"当前页面不存在章节数据"
            raise Exception,u"当前页面不存在章节数据"
    def test_05_bear_student_chapterFinish(self):
        """ 视频播放完毕后更新学习完成状态<br>https://mobile.yunshuxie.com/v1/bear/student/chapterFinish.htm<br/>{"productChapterId":"","isApp":"2"}"""
        productChapterId = self.redis.str_get("bearWord_productChapterId") if self.redis.str_get("bearWord_productChapterId") else None
        if productChapterId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/chapterFinish.htm"
            params = {"productChapterId":productChapterId,"isApp":"2"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = self.session.post(url=url, data=params)
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
            print u"当前页面不存在章节数据"
            raise Exception,u"当前页面不存在章节数据"
    def test_06_bear_student_uploadWork(self):
        """ 上传作品<br>https://mobile.yunshuxie.com/v1/bear/student/uploadWork.htm<br/>{img,content,productChapterId,isApp}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过上传作品接口"
        else:
            productChapterId = self.redis.str_get("bearWord_productChapterId") if self.redis.str_get("bearWord_productChapterId") else None
            if productChapterId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/uploadWork.htm"
                params = {"img":"https://ysx-sts-upload.oss-cn-beijing.aliyuncs.com/pic/ios/avatar/2019/07/26/14/44/15/f0611a93e0034d5ab5ebc0c86dc4046c/D373EF8C-8F81-47F2-83FC-8B072F536EEB.png",
                          "content":"测试,权限归测试组所有",
                          "productChapterId":productChapterId,"isApp":"2"}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
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
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"
    def test_07_bear_student_clock(self):
        """ 打卡接口<br>https://mobile.yunshuxie.com/v1/bear/student/clock.htm<br/>{img,content,productChapterId,isApp}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过打卡接口"
        else:
            productCourseId = self.redis.str_get("bearWord_productCourseId") if self.redis.str_get("bearWord_productCourseId") else None
            productChapterId = self.redis.str_get("bearWord_productChapterId") if self.redis.str_get("bearWord_productChapterId") else None
            if productCourseId and productChapterId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/uploadWork.htm"
                params = {"productCourseId":productCourseId,"productChapterId":productChapterId,"isApp":"2"}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
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
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"
    def test_08_bear_student_uploadWork(self):
        """重新上传作品<br>https://mobile.yunshuxie.com/v1/bear/student/uploadWork.htm<br/>{img,content,productChapterId,isApp}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过上传作品接口"
        else:
            productChapterId = self.redis.str_get("bearWord_productChapterId") if self.redis.str_get("bearWord_productChapterId") else None
            if productChapterId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/uploadWork.htm"
                params = {"img":"https://ysx-sts-upload.oss-cn-beijing.aliyuncs.com/pic/ios/avatar/2019/07/26/14/44/15/f0611a93e0034d5ab5ebc0c86dc4046c/D373EF8C-8F81-47F2-83FC-8B072F536EEB.png",
                          "content":"测试重复上传,权限归测试组所有",
                          "productChapterId":productChapterId,"isApp":"2"}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
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
                if result["data"]["workId"]:
                    workId = self.redis.str_set("bearWord_workId",result["data"]["workId"])
                else:
                    self.redis.del_key("bearWord_workId")
            else:
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"
    def test_09_bear_teacher_reject_job(self):
        """作业退回接口-教师端<br>https://mobile.yunshuxie.com/v1/bear/teacher/return_job.htm<br/>{"timeLineId":""}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过打卡接口"
        else:
            workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
            if workId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/teacher/return_job.htm"
                params = {"timeLineId":workId}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
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
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"
    def test_10_bear_teacher_reject_job(self):
        """ 驳回接口-教师端<br>https://mobile.yunshuxie.com/v1/bear/teacher/reject_job.htm<br/>{"timeLineId":"","reasonId":"","status":""}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过打卡接口"
        else:
            workId = self.redis.str_get("bearWord_workId") if self.redis.str_get("bearWord_workId") else None
            if workId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/teacher/reject_job.htm"
                params = {"timeLineId":workId,"reasonId":"1","status":"1"}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
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
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()