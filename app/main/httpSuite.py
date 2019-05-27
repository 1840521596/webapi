#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ = "guohongjie"
from flask import make_response,request,flash,jsonify
from . import test
from ..base.pythonProject import run
from .. import db
from ..config.models import Project,Test_Env
from ..config.sendMsg import sendMsg
@test.route("/runSuiteApi",methods=["GET"])
def runDatasApiTest():
	"""测试集页面使用接口,用于上传测试用例后执行
	:param project:  测试项目
	:param env_num:  测试环境编号
	:param env_flag:  测试环境
	:return:  msg: 执行状态
	"""
	project = request.args.get("project")
	env_num = request.args.get("env_num")
	env_flag = request.args.get("env_flag")
	from getConfig import s
	s.add_set("ENV", env_num=env_num, env_flag=env_flag)
	try:
		project_en = db.session.query(Project.project_en,Project.description).filter_by(project=project).first()
		run.run_test_case(project_en[0],env_num,env_flag,project_en[1],project)
		msg = {"code":200,"Msg":"执行成功"}
	except Exception as e:
		msg = {"code":400,"Msg":"执行失败","ErrorMsg":str(e)}
	return make_response(jsonify(msg))


@test.route("/runSuiteApi_yunwei",methods=["GET"])
def runDatasApiTest_yunwei():
	"""运维发布版本后使用接口
	:param project:  测试项目
	:param env_num:  测试环境编号
	:param env_flag:  测试环境
	:return:  msg: 执行状态
	"""
	project = request.args.get("project")
	env_num = request.args.get("env_num")
	env_flag = request.args.get("env_flag")
	from getConfig import s
	s.add_set("ENV",env_num=env_num,env_flag=env_flag)
	try:
		project_en = db.session.query(Project.project_en, Project.description).filter_by(project=project).first()
		if project_en:
			result = run.run_yunwei_case(project_en[0],env_num,env_flag,project_en[1],project)
			msg = {"code":200,"Msg":"执行成功","url":r"http://uwsgi.sys.bandubanxie.com/Report",
				   "Error":result["Error"],"Failure":result["Failure"],"Success":result["Success"]}
			if result["Error"] != 0 or result["Failure"] !=0:
				message = """《{project_cn}》接口测试报告存在失败用例，请访问 http://uwsgi.sys.bandubanxie.com/Report 查看，错误数量：{error} 个""".format(project_cn=project,error=result["Error"])
				sendMsg(message,["18519118952"])
		else:
			raise Exception("{project}不存在".format(project=project))
	except Exception as e:
		msg = {"code":400,"Msg":"执行失败","ErrorMsg":str(e)}
	return make_response(jsonify(msg))


@test.route("/make_user",methods=["GET"])
def make_user():
	"""测试页面使用接口,用于创建测试账号执行
    	:param env_num:  测试环境编号
    	:param env_flag:  测试环境
    	:param phones: 测试手机号
    	:param user_role: 测试角色
    	:return:  msg: 执行状态
    	"""
	env_num = request.args.get("env_num")
	env_flag = request.args.get("env_flag")
	phones = request.args.get("phones")
	user_role = request.args.get("user_role")
	if len(user_role.split(",")) != len(phones.split(",")):
		raise Exception("用户手机号和用户角色数量不等")
	from getConfig import s
	s.add_set("ENV", env_num=env_num, env_flag=env_flag)
	s.add_set("PARAMS", phoneNumList=phones, employeeTypes=user_role)
	try:
		result = run.run_yunwei_case("make_user", env_num, env_flag, "Admin 创建用户：{phones}".format(phones=phones), "创建测试用户")
		msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
			   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
	except Exception as e:
		msg = {"code": 400, "Msg": "执行失败", "ErrorMsg": str(e)}
	return make_response(jsonify(msg))





@test.route("/searchEnvNum",methods=["GET"])
def searchEnvNum():
	env_flag = request.args.get("env_flag")
	env_num = db.session.query(Test_Env.env_num).filter_by(env_flag=env_flag).all()
	msg = {"code":200,"msg":env_num}
	return make_response(jsonify(msg))