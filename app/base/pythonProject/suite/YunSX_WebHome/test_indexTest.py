#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from requests import Session,Request
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
logging = TestLog().getlog()
class indexTestTest(unittest.TestCase):
    #"indexTest"
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        env_flag = s.get_env("env_flag")
        env_num = s.get_env("env_num")
        phoneNum = s.get_params("phoneNum")
        userName = s.get_admin("userName")
        pwd = s.get_admin("pwd")
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('env_flag', env_flag)  #设置测试环境
        self.cookies.set("env_num",env_num)  #设置环境号
        
        data = {"userName":"13500000023","pwd":"123456"}
        self.url = "https://www.yunshuxie.com"+"/v5/web/account/login.htm"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.post(self.url, data=data, headers=caseHeaders ,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        self.cookies.update(self.resp.cookies)
    
    def test_login_faile(self):
        """登录失败"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"-3","returnMsg":"系统错误","data":{}}
        data = {"userName":"123","pwd":"ghj123"}
        self.url = "https://www.yunshuxie.com"+"/v5/web/account/login.htm"
        method = "POST"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.post(self.url, data=data, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        def assertKey(value1,value2):
            dictvalue1 = value1
            dictvalue2 = value2
            if type(dictvalue2).__name__ == "dict":
                for key,value in dictvalue2.items():
                    if dictvalue1.has_key(key):
                        if type(value).__name__ == "dict":
                            assertKey(dictvalue1[key],dictvalue2[key])
                        elif type(value).__name__ == "list":
                            assertKey(dictvalue1[key],dictvalue2[key])
                    else:
                        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""
                        return key
            elif type(dictvalue2).__name__ == "list":
                for list_index in range(len(dictvalue2)):
                    assertKey(dictvalue1[list_index],dictvalue2[list_index])
        value1 = self.caseExpectDatas
        value2 = json.loads(re.match(".*?({.*}).*", self.resp.content, re.S).group(1))
        keyValue = assertKey(value1,value2)
        if keyValue:
            assert keyValue=="Error",msg.format(Except=keyValue,Really="Error")
    def test_03_hello_teacher(self):
        """查看老师好页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/laoshihao.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_04_tester(self):
        """查看json数据"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":{"otherPowerValue":"0","checkValue":"0","shareNum":"0","courseValue":"","myClassList":[{"moocClassId":"516699","moocClassName":"升级版每日一句(五年级)-24班"},{"moocClassId":"517140","moocClassName":"【B端测试课程】呐喊-1班(2018-02-26)"},{"moocClassId":"494046","moocClassName":"0623_北街小学"},{"moocClassId":"624801","moocClassName":"每日一段作文素材课(初中)-二期-54班(2019-01-28)"}],"allPowerValue":"0","myCourseListData":{"total":"0","mysqlStartRow":"0","pageCount":"0","page":"1","condition":{"memberId":"1280040"},"pageSize":"5","list":[]},"powerValueRankingList":[{"nickName":"王绎宁","memberId":"147576","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/05/01/08/1493600124698.jpg","powerValue":"23993"},{"nickName":"王耀贤","memberId":"70217","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/10/24/08/1540340867877.jpg","powerValue":"23594"},{"nickName":"唐亦飞","memberId":"147573","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/04/19/22/1492612639263.jpg","powerValue":"20327"},{"nickName":"静怡","memberId":"29745","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/07/28/20/1532779695171.jpg","powerValue":"18653"},{"nickName":"马若霏","memberId":"147568","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/04/19/20/1492605887022.jpg","powerValue":"13812"},{"nickName":"文轩","memberId":"18571","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/11/24/19/1543060700471.jpg","powerValue":"13496"},{"nickName":"IFAB","memberId":"77371","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2019/02/24/18/1551003317548.jpg","powerValue":"13342"},{"nickName":"岳朋伯","memberId":"151569","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/03/30/20/1522413482501.jpg","powerValue":"11379"},{"nickName":"喻佳琦","memberId":"95050","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2019/02/09/19/1549710953596.jpg","powerValue":"10038"},{"nickName":"王新彦","memberId":"41761","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/08/19/07/1534636405687.jpg","powerValue":"9431"},{"nickName":"肖亦航","memberId":"147827","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/04/26/21/1493215028811.jpg","powerValue":"9350"},{"nickName":"PATRICK","memberId":"43947","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/02/06/12/1517891936975.png","powerValue":"9099"},{"nickName":"雅欣","memberId":"100436","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/10/04/12/1538629096777.jpg","powerValue":"9088"},{"nickName":"柴梦萱","memberId":"147683","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/04/19/20/1492606095036.jpg","powerValue":"8698"},{"nickName":"杨沁","memberId":"42189","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/05/20/16/1526806291632.jpg","powerValue":"7686"},{"nickName":"聂佳宁","memberId":"22439","headPic":"https://thirdwx.qlogo.cn/mmopen/vi_32/NwUm8l667t5ianeINZzqHnb5q6Yiaaibkrz9YIqr2ccAkxYTictegMAkKqFibgDtZJibLnODVMQecz0HXOTibasRUiaCAA/132","powerValue":"7483"},{"nickName":"徐安","memberId":"94632","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2018/08/25/20/1535198446557.jpg","powerValue":"6997"},{"nickName":"宋泓锐","memberId":"96486","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/06/26/20/1498481845106.jpg","powerValue":"6965"},{"nickName":"于沐菲","memberId":"69942","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2017/07/13/17/1499939315029.jpg","powerValue":"6488"},{"nickName":"严允诺","memberId":"14562","headPic":"https://oss-ysx-pic.yunshuxie.com/head-icon/2016/12/22/07/1482364489439.jpg","powerValue":"6320"}],"courseNum":"1","jobNum":"0"}}
        params = json.dumps({"page":"1","pageSize":"5","callback": "_jsonpc5o0h5fyroa"})
        self.url = "https://www.yunshuxie.com"+"/v2/read_statistics/myRead_statistics.htm?page=1&pageSize=5&callback=_jsonpc5o0h5fyroa"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        respMsg = self.resp.content  #返回值
        caseExpectDatas = self.caseExpectDatas  #xls 校验值
        if caseExpectDatas:
            if type(caseExpectDatas).__name__ == "str":
                assert caseExpectDatas==respMsg,msg.format(Except=caseExpectDatas,Really=respMsg)
            elif type(caseExpectDatas).__name__ == "dict":
                json_caseExpectDatas = json.dumps(caseExpectDatas, encoding='utf-8', ensure_ascii=False)  # 期望值转换json
                try:
                    dict_resp = json.loads(re.match(".*?({.*}).*", respMsg, re.S).group(1))
                    assert caseExpectDatas==dict_resp,msg.format(Except=json_caseExpectDatas, Really=respMsg)  #判断期望值==返回值(转换成字典)
                except Exception as e:  #当value2 不是json类型
                    print e
                    respMsg = re.match(".*?({.*}).*", respMsg, re.S).group(1)
                    assert json_caseExpectDatas == respMsg,msg.format(Except=json_caseExpectDatas, Really=respMsg)

    def test_05_course(self):
        """查看课程体系页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/coursesys.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_06_blend_read(self):
        """查看课程体系页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/wholeBook.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_07_student_story(self):
        """查看课程体系页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/v1/web/ststory.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_08_teacher_team(self):
        """查看课程体系页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/v1/web/teacher.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_09_school_order(self):
        """查看课程体系页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/v1/web/school.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    def test_10_deep_learn(self):
        """查看课程体系页面"""
        self.caseStatusCode = 200
        self.caseExpectDatas =None
        params = None
        self.url = "https://www.yunshuxie.com"+"/v1/web/resultspc.htm"
        method = "GET"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = """
        Except:  {Except}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        #不用校验返回值
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        
        pass
if __name__ == "__main__":
    unittest.main()