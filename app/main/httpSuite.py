#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ = "guohongjie"
from flask import make_response,request,flash,jsonify
import requests
from . import test
from ..base.pythonProject import run
from .. import db,redis
from ..config.models import Project,Test_Env,Test_User_Reg
from ..config.sendMsg import sendMsg
from sqlalchemy import func
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
	# from getConfig import s
	# s.add_set("ENV",env_num=env_num,env_flag=env_flag)
	try:
		project_en = db.session.query(Project.project_en, Project.description).filter_by(project=project).first()
		if env_flag in ["stage","prod"]:
			new_env_flag = ",".join(["stage","prod"])
		else:
			new_env_flag = "beta"
		new_phone = int(db.session.query(func.max(Test_User_Reg.phone)).filter_by(env=new_env_flag).first()[0]) + 1 #最大手机号+1
		print new_phone
		if project_en:
			redis_env_flag_shell = "{project_en}_env_flag".format(project_en=project_en[0])
			redis_env_num_shell = "{project_en}_env_num".format(project_en=project_en[0])
			redis.set(redis_env_flag_shell,env_flag)
			redis.set(redis_env_num_shell,env_num)
			redis.set("make_user_env_flag", env_flag)
			redis.set("make_user_env_num", env_num)
			redis.set("make_user_phones", "%d"%new_phone)
			redis.set("make_user_employeetypes", "0")
			result = run.run_yunwei_case("make_user", env_num, env_flag,
										 "Admin 创建用户：{phones}".format(phones=new_phone), "创建测试用户")
			if result["Error"] == 0 and result["Failure"] == 0:  # 成功创建用户后，数据库记录
				try:
					datas = Test_User_Reg(phone="%d"%new_phone, type="0", env=new_env_flag)
					db.session.add(datas)
					db.session.commit()
				except Exception as e:
					db.session.rollback()
				result = run.run_yunwei_case(project_en[0],env_num,env_flag,project_en[1],project)
				if result["Error"] != 0 or result["Failure"] !=0:
					message = """《{project_cn}》接口测试报告存在失败用例，请访问 http://uwsgi.sys.bandubanxie.com/Report 查看，脚本错误数量：{error} 个;失败数量：{failure}""".format(project_cn=project,error=result["Error"],failure=result["Failure"])
					#sendMsg(message,["18519118952","15201532513","18010136420","13520170386"]) # 郭宏杰  王梦晓  洪琛  张红铃
				else:
					msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
					   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
			else:
				msg = {"code":400,"Msg":"执行失败","ErrorMsg":"用户手机号创建失败"}
		else:
			raise Exception("{project}不存在".format(project=project))
	except Exception as e:
		msg = {"code":400,"Msg":"执行失败","ErrorMsg":str(e)}
	return make_response(jsonify(msg))
	#return "ok"


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
	phones = request.args.get("phones").split(",")
	user_role = request.args.get("user_role").split(",")
	if len(user_role) != len(phones):
		raise Exception("用户手机号和用户角色数量不等")
	# from getConfig import s
	# s.add_set("ENV", env_num=env_num, env_flag=env_flag)
	# s.add_set("PARAMS", phoneNumList=phones, employeeTypes=user_role)
	try:
		redis.set("make_user_env_flag",env_flag)
		redis.set("make_user_env_num", env_num)
		redis.set("make_user_phones",",".join(phones))
		redis.set("make_user_employeetypes",",".join(user_role))
		result = run.run_yunwei_case("make_user", env_num, env_flag, "Admin 创建用户：{phones}".format(phones=",".join(phones)), "创建测试用户")
		if result["Error"] == 0 and result["Failure"] == 0:  #成功创建用户后，数据库记录
			msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
			   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
			for num in range(len(phones)):
				try:
					if env_flag in ["stage","prod"]:
						env_flag = ",".join(["stage","prod"])
					datas = Test_User_Reg(phone=phones[num],type=user_role[num],env=env_flag)
					db.session.add(datas)
					db.session.commit()
				except Exception as e:
					db.session.rollback()
					msg = {"code": 204, "datas": str(e)}
		else:
			msg = {"code": 400, "Msg": "执行失败", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
				   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}

	except Exception as e:
		msg = {"code": 4004, "Msg": "执行失败", "ErrorMsg": str(e)}
	return make_response(jsonify(msg))






@test.route("/searchEnvNum",methods=["GET"])
def searchEnvNum():
	env_flag = request.args.get("env_flag")
	env_num = db.session.query(Test_Env.env_num).filter_by(env_flag=env_flag).all()
	msg = {"code":200,"msg":env_num}
	return make_response(jsonify(msg))