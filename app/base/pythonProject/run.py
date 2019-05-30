#!/usr/bin/python
#-*-coding:utf-8 -*-
import unittest
from base import HTMLTestRunnerCN
from base.makeSuite import MakeTestSuite
import datetime
import os
# 测试用例存放路径
# 获取所有测试用例
TEST_FOLDER = "./app/base/pythonProject"
def get_allcase(project):
    """
    :param project:  传入{project},获得suite路径下{project}文件夹内test开头的py文件
    :return: suite:  测试集合
    """
   # print TEST_FOLDER +"/suite/{project}".format(project=project)
    case_path = os.path.join(TEST_FOLDER +"/suite/",project)
    dis = unittest.TestLoader()
    discover = dis.discover(case_path, pattern="test*.py")

    suite = unittest.TestSuite()
    suite.addTest(discover)
    return suite
def run_test_case(project_en,env_num,env_flag,description,project_cn):
    """
    :param project:  传入{project},创建 suite路径/test_setting路径下{project}文件夹
    :param env_num:  测试环境号
    :param env_flag:  测试环境
    :return:  测试报告
    """
    # 运行测试用例
    xls_path = TEST_FOLDER + "/test_setting/{project}".format(project=project_en)
    filepath = TEST_FOLDER + "/suite/{project}".format(project=project_en)
    MakeTestSuite(xls_path).make_template(filepath)
    #year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    filePath = TEST_FOLDER + "/ReportHtml/{month}/{day}".format(month=month,day=day)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    fileName = "{project}.html".format(project=project_cn)
    fp = filePath+"/"+fileName
    fp = file(fp,"wb")
    runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title="《"+project_cn+"》--接口测试报告", description=description,env_num=env_num,env_flag=env_flag)
    runner.run(get_allcase(project_en))


def run_yunwei_case(project_en,env_num,env_flag,description,project_cn,**kwargs):
    """
    :param project:  传入{project},创建 suite路径/test_setting路径下{project}文件夹
    :param env_num:  测试环境号
    :param env_flag:  测试环境
    :return:  测试报告
    """
    # 运行测试用例
    filepath = TEST_FOLDER + "/suite/{project}".format(project=project_en)
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    filePath = TEST_FOLDER + "/ReportHtml/{month}/{day}".format(month=month,day=day)
    fileName = "{project}_{env_flag}.html".format(project=project_cn, env_flag=env_flag)
    # if env_num:
    #     fileName = "{project}_{env_flag}_{env_num}.html".format(project=project_cn,env_flag=env_flag,env_num=env_num)
    # else:
    #     fileName = "{project}_{env_flag}.html".format(project=project_cn, env_flag=env_flag)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    fp = filePath+"/"+fileName
    fp = file(fp,"wb")
    runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title="《"+project_cn+"》--接口测试报告", description=description,env_num=env_num,env_flag=env_flag)
    test_result = runner.run(get_allcase(project_en))
    error_count,failure_count,success_count =test_result.error_count,test_result.failure_count,test_result.success_count
    return {"Error":error_count,"Failure":failure_count,"Success":success_count}