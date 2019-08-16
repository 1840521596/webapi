#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ = "guohongjie"
from flask import make_response,request,jsonify,url_for,redirect
from . import test
from ..base.pythonProject import run
from .. import db,redis
from ..config.models import Project,Test_Env,Test_User_Reg
from sqlalchemy import func
from app.base.pythonProject.base.getConfig import s
from app.base.pythonProject.base.couponReceive import coupon_test
import redis as red
from threading import Thread
import json
from ..tasks.tasks import run_api
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
	s.add_set("ENV",env_num=env_num,env_flag=env_flag)
	try:
		project_en = db.session.query(Project.project_en,Project.description).filter_by(project=project).first()
		redis_env_flag_shell = "{project_en}_env_flag".format(project_en=project_en[0])
		redis_env_num_shell = "{project_en}_env_num".format(project_en=project_en[0])
		redis.set(redis_env_flag_shell, env_flag)
		redis.set(redis_env_num_shell, env_num)
		run.run_test_case(project_en[0],env_num,env_flag,project_en[1],project)
		msg = {"code":200,"Msg":"执行成功"}
	except Exception as e:
		msg = {"code":400,"Msg":"执行失败","ErrorMsg":str(e)}
	return make_response(jsonify(msg))
# @test.route("/runSuiteApi_yunwei",methods=["GET"])
# def runDatasApiTest_yunwei():
# 	"""运维发布版本后使用接口
# 	:param project:  测试项目
# 	:param env_num:  测试环境编号
# 	:param env_flag:  测试环境
# 	:return:  msg: 执行状态
# 	"""
# 	chose_run = {}
# 	project = request.args.get("project")
# 	env_num = request.args.get("env_num")
# 	env_flag = request.args.get("env_flag")
# 	s.add_set("ENV", env_num=env_num, env_flag=env_flag) #云舒写首页&admin 会使用config.ini配置文件
# 	redis_host = s.get_env("beta").split(":") if env_flag == "beta" else s.get_env("prod_stage").split(":")
# 	r = red.Redis(host=redis_host[0], port=int(redis_host[1]), password="yunshuxie1029Password")
# 	r.set("021ZaJtG17hM310SblvG1NZutG1ZaJtQ",'o38sIv_7FQInsBKJEUExn7wYxoHc&21_bk4dQIEFnYz5w8zJwDqan84UFmV_XVKEO5MJf7fv1pGR8tRH2MAtxpk0Pc1SqDwe5S90CE6TQo1wd346qEA5FQ')
# 	try:
# 		project_en = db.session.query(Project.project_en, Project.description).filter_by(project=project).first()
# 		if project_en:
# 			redis_env_flag_shell = "{project_en}_env_flag".format(project_en=project_en[0])
# 			redis_env_num_shell = "{project_en}_env_num".format(project_en=project_en[0])
# 			redis.set(redis_env_flag_shell,env_flag)
# 			redis.set(redis_env_num_shell,env_num)
# 			if "admin".upper() not in project_en[0].upper() and "crm".upper() not in project_en[0].upper():  #判断项目内容，新增测试用户
# 				try:
# 					if env_flag in ["stage", "prod"]:
# 						new_env_flag = ",".join(["stage", "prod"])
# 					else:
# 						new_env_flag = "beta"
# 					new_phone = str(int(db.session.query(func.max(Test_User_Reg.phone)).filter_by(env=new_env_flag).first()[0]) + 1)  # 最大手机号+1
# 					redis.set("make_user_env_flag", env_flag)
# 					redis.set("make_user_env_num", env_num)
# 					redis.set("make_user_phones", new_phone)
# 					redis.set("make_user_employeetypes", "0")
# 					result = run.run_yunwei_case("make_user", env_num, env_flag,
# 											 "Admin 创建用户：{phones}".format(phones=new_phone), "创建测试用户")
# 					datas = Test_User_Reg(phone=new_phone, type="0", env=new_env_flag)
# 					db.session.add(datas)
# 					db.session.commit()
# 					chose_run["new_phone"] = new_phone
# 				except Exception as e:
# 					db.session.rollback()
# 					raise Exception("ErrorMsg: 用户手机号创建失败{phone}".format(phone=new_phone))
# 					#msg = {"code":400,"Msg":"执行失败","ErrorMsg":"ErrorMsg: 用户手机号创建失败{phone}".format(phone=new_phone)}
# 			if chose_run.has_key("new_phone"):  #字典内存在新用户号码，传入新手机号
# 				result = run.run_yunwei_case(project_en=project_en[0],env_num=env_num,env_flag=env_flag,description=project_en[1],
# 											 project_cn=project,new_phone=chose_run["new_phone"])
# 			else:
# 				result = run.run_yunwei_case(project_en=project_en[0], env_num=env_num,
# 											 env_flag=env_flag, description=project_en[1],project_cn=project)
# 			if result["Error"] != 0 or result["Failure"] !=0:  #执行反馈存在错误和失败，短信通知
# 				message = """《{project_cn}》接口测试报告存在失败用例，请访问 http://uwsgi.sys.bandubanxie.com/Report 查看，脚本错误数量：{error} 个;失败数量：{failure}""".format(project_cn=project,error=result["Error"],failure=result["Failure"])
# 				sendMsg(message,["18519118952"]) # 郭宏杰  王梦晓  洪琛  张红铃
# 				#sendMsg(message,["18519118952","15201532513","18010136420","13520170386"]) # 郭宏杰  王梦晓  洪琛  张红铃
# 				msg = {"code": 400, "Msg": "接口测试成功，存在未通过项", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
# 				   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
# 			else:
# 				msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
# 					   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
# 		else:
# 			raise Exception("{project}不存在".format(project=project))
# 	except Exception as e:
# 		msg = {"code":400,"Msg":"执行失败","ErrorMsg":str(e)}
# 	return make_response(jsonify(msg))
@test.route("/runSuiteApi_yunwei",methods=["GET"])
def runDatasApiTest_yunwei():
	"""运维发布版本后使用接口
	:param project:  测试项目
	:param env_num:  测试环境编号
	:param env_flag:  测试环境
	:return:  msg: 执行状态
	"""
	chose_run = {}
	project = request.args.get("project")
	env_num = request.args.get("env_num")
	env_flag = request.args.get("env_flag")
	developer = request.args.get("developer")
	developer_project = request.args.get("developer_project")
	branch = request.args.get("branch")
	try:
		if env_flag != "beta":
			raise Exception("当前环境非测试环境！")
		if project == "":
			raise Exception("项目不能为空！")
		if env_num == "":
			raise Exception("环境编号不能为空！")
		if env_flag == "":
			raise Exception("使用环境不能为空！")
		project_en = db.session.query(Project.project_en, Project.description).filter_by(project=project,use_status=1).first()  #查询项目
		if project_en:  #判断项目存在
			redis_env_flag_shell = "{project_en}_env_flag".format(project_en=project_en[0])
			redis_env_num_shell = "{project_en}_env_num".format(project_en=project_en[0])
			redis.set(redis_env_flag_shell,env_flag)  #设置测试环境
			redis.set(redis_env_num_shell,env_num)  #设置环境号码
			s.add_set("ENV", env_num=env_num, env_flag=env_flag) #云舒写首页&admin 会使用config.ini配置文件
			redis_host = s.get_env("beta").split(":") if env_flag == "beta" else s.get_env("prod_stage").split(":")
			r = red.Redis(host=redis_host[0], port=int(redis_host[1]), password="yunshuxie1029Password")
			r.set("021ZaJtG17hM310SblvG1NZutG1ZaJtQ",'o38sIv_7FQInsBKJEUExn7wYxoHc&21_bk4dQIEFnYz5w8zJwDqan84UFmV_XVKEO5MJf7fv1pGR8tRH2MAtxpk0Pc1SqDwe5S90CE6TQo1wd346qEA5FQ')
			if "admin".upper() not in project_en[0].upper() and "crm".upper() not in project_en[0].upper() and "wacc_tortoise".upper() not in project_en[0].upper():  # 判断项目不等于admin&&crm，新增测试用户
				try:
					if env_flag in ["stage", "prod"]:
						new_env_flag = ",".join(["stage", "prod"])
					else:
						new_env_flag = "beta"
					new_phone = str(int(db.session.query(func.max(Test_User_Reg.phone)).filter_by(env=new_env_flag).first()[0]) + 1)  # 最大手机号+1
					redis.set("make_user_env_flag", env_flag)
					redis.set("make_user_env_num", env_num)
					redis.set("make_user_phones", new_phone)
					redis.set("make_user_employeetypes", "0")
					result = run.run_yunwei_case("make_user", env_num, env_flag,
											 "Admin 创建用户：{phones}".format(phones=new_phone), "创建测试用户",
												 new_phone=new_phone,developer=developer,developer_project=developer_project,branch=branch)
					datas = Test_User_Reg(phone=new_phone, type="0", env=new_env_flag,description=project)  #新建手机号码存储至数据库
					db.session.add(datas)
					db.session.commit()
					chose_run["new_phone"] = new_phone
				except Exception as e:
					db.session.rollback()
					raise Exception("ErrorMsg: 用户手机号创建失败{phone}".format(phone=new_phone))
				else:
					if chose_run.has_key("new_phone"):  #字典内存在新用户号码，传入新手机号
						process = Thread(target=run.run_yunwei_case,name="",
										  args=(project_en[0],env_num,env_flag,project_en[1],project,chose_run["new_phone"],
												developer,developer_project,branch))
						process.start()
						msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report"}
			else:
				chose_run["new_phone"] = None
				process = Thread(target=run.run_yunwei_case,args=(project_en[0],env_num,env_flag,project_en[1],project,
																  chose_run["new_phone"],developer,developer_project,branch))
				process.start()
				msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report"}
			# if result["Error"] != 0 or result["Failure"] !=0:  #执行反馈存在错误和失败，短信通知
			# 	message = """《{project_cn}》接口测试报告存在失败用例，请访问 http://uwsgi.sys.bandubanxie.com/Report 查看，脚本错误数量：{error} 个;失败数量：{failure}""".format(project_cn=project,error=result["Error"],failure=result["Failure"])
			# 	sendMsg(message,["18519118952"]) # 郭宏杰  王梦晓  洪琛  张红铃
			# 	#sendMsg(message,["18519118952","15201532513","18010136420","13520170386"]) # 郭宏杰  王梦晓  洪琛  张红铃
			# 	msg = {"code": 400, "Msg": "接口测试成功，存在未通过项", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
			# 	   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
			# else:
			# 	msg = {"code": 200, "Msg": "执行成功", "url": r"http://uwsgi.sys.bandubanxie.com/Report",
			# 		   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
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
	phones = request.args.get("phones").split(",")
	user_role = request.args.get("user_role").split(",")
	try:
		if phones[0]=="":
			raise Exception("用户手机号不能为空！")
		else:
			for phone in phones:
				if len(phone) != 11:
					raise Exception("用户手机号需等于11位！")
		if env_flag=="":
			raise Exception("使用环境不能为空！")
		if len(user_role) != len(phones):
			raise Exception("用户手机号和用户角色数量不等！")
		redis.set("make_user_env_flag",env_flag)
		redis.set("make_user_env_num", env_num)
		redis.set("make_user_phones",",".join(phones))
		redis.set("make_user_employeetypes",",".join(user_role))
		result = run.run_yunwei_case("make_user", env_num, env_flag, "Admin 创建用户：{phones}".format(phones=",".join(phones)), "创建测试用户",
									 new_phone=",".join(phones))
		if result["Error"] == 0 and result["Failure"] == 0:  #成功创建用户后，数据库记录
			msg = {"code": 200, "Msg": "执行成功", "url": result["report_url"],
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
			msg = {"code": 400, "Msg": "执行失败", "url": result["report_url"],
				   "Error": result["Error"], "Failure": result["Failure"], "Success": result["Success"]}
	except Exception as e:
		msg = {"code": 400, "Msg": "执行失败", "ErrorMsg": str(e)}
	return make_response(jsonify(msg))
@test.route("/get_coupon",methods=["GET"])
def get_coupon():
	"""
	领取代金券接口,传入测试环境&测试环境号&代金券价格&手机号码，领取10张当天使用的优惠券
	:return:
	"""
	env_num = request.args.get("env_num")
	env_flag = request.args.get("env_flag")
	couponPrice = request.args.get("couponPrice")
	phone = request.args.get("phone")
	try:
		if env_flag == "":
			raise Exception("使用环境不能为空！")
		if couponPrice == "":
			raise Exception("代金券价格不能为空！")
		if phone == "":
			raise Exception("领取手机号不能为空！")
		if len(phone) != 11:
			raise Exception("领取手机号需等于11位！")
		if env_flag in ["stage", "prod"]:
			select_env_flag = ",".join(["stage", "prod"])
		else:
			select_env_flag = "beta"
		datas = db.session.query(Test_User_Reg.description).filter_by(phone=phone, env=select_env_flag).count()
		if datas == 0:
			raise Exception("手机号未存在于号码管理页面，请先增加该用户")
		resp = coupon_test(env_flag=env_flag,env_num=env_num,couponPrice=couponPrice,phone=phone)
		desc = json.dumps(resp["coupins_desc"],ensure_ascii=False,encoding="utf8")
		datas = db.session.query(Test_User_Reg.id,Test_User_Reg.description).filter_by(phone=phone, env=select_env_flag).first()
		d = datas[1] if datas[1] else ""
		description = d +"<br/>"+desc
		Test_User_Reg.query.filter_by(id=datas[0]).update(dict(phone=phone,description=description))
		db.session.commit()
	except Exception as e:
		msg = {"code": 400, "Msg": "执行失败", "ErrorMsg": str(e)}
	else:
		msg = {"code": 200, "Msg": "执行成功", "ReturnMsg": resp}
	return make_response(jsonify(msg))
@test.route("/searchEnvNum",methods=["GET"])
def searchEnvNum():
	env_flag = request.args.get("env_flag")
	env_num = db.session.query(Test_Env.env_num).filter_by(env_flag=env_flag).all()
	msg = {"code":200,"msg":env_num}
	return make_response(jsonify(msg))




@test.route("/runSchedule",methods=["POST"])
def run_schedule():
	"""
	运行web端录入接口调度
	:param: project 测试项目
	:return:
	"""
	project = "云舒写后台管理系统" #request.args.get("project").strip()
	developer = u"guohongjie"
	num = 10#request.args.get("num") if request.args.get("num") else None
	task = run_api.apply_async(args=[project,developer],countdown=num)
	return jsonify({}), 202, {'Location': url_for('test.taskstatus',task_id=task.id)}


@test.route('/status/<task_id>')
def taskstatus(task_id):
	task = run_api.AsyncResult(task_id)
	if task.state == 'PENDING':
		response = {
			'state': task.state,
			'current': 0,
			'total': 1,
			'status': u'启动中...'
		}
	elif task.state != 'FAILURE':
		response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': task.info.get('total', 1),
			'status': task.info.get('status', ''),
			'pass_status':task.info.get('pass_status',''),
			'datas':task.info.get('data_list','')
		}
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info),  # this is the exception raised
		}
	return jsonify(response)

















@test.route("/phones",methods=["GET"])
def phones():
	phones = db.session.query(Test_User_Reg.phone).all()
	list_phone = []
	for phone in phones:
		list_phone.append(phone[0])
	return jsonify(",".join(list_phone))

