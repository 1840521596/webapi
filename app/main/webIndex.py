#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify,session,g
from .. import db,redis
from flask_login import login_required
from ..config.api_models import Project, Case_Http_API,Web_Model_Set,Test_User_Reg,Key_Value
@views.route("/webIndex",methods=["GET"])
@login_required
def webIndex():
    """WEB首页"""
    modelNameLink = db.session.query(Web_Model_Set.modelName,Web_Model_Set.modelLink).filter_by(modelStatus=1).order_by("id").all()
    modelList = [[m[0],m[1]] for m in modelNameLink]
    userName = session["userName"]
    deptName = session["deptName"]
    projectCount = db.session.query(Project.id).count()
    interfaceCount = db.session.query(Case_Http_API.id).count()
    return render_template('home/index.html', modelNameLink=modelList,project_cout=projectCount,jiekou=interfaceCount,
                           userName=userName,deptName=deptName)
                           #report=len(reslut_list), project_cout=project_cout,
                         #  model_cout=model_cout, my_tasl=My_task, all_run_case_count=all_run_case_count

@views.route("/homeIndex",methods=["GET"])
@login_required
def homeIndex():
    return render_template('home/homeIndex.html')
@views.route("/index",methods=["GET"])
@login_required
def index():
    return render_template('home/homeIndex.html')
@views.route("/pageIndex",methods=["GET"])
@login_required
def pageIndex():
    return render_template('home/pageIndex.html')
@views.route("/testIndex",methods=["GET"])
@login_required
def testIndex():
    return render_template('home/test_phones.html')
@views.route('/run_api_index', methods=['GET', 'POST'])
@login_required
def run_api_index():
    api_project = Project.query.with_entities(Project.project).distinct().all()
    return render_template('/home/run_api_index.html',projects=api_project)
@views.route("/query_phones",methods=["GET"])
@login_required
def test_query():
    """Test_Phones"""
    query_phone = request.args.get("PHONE")
    env = request.args.get("ENV")
    if query_phone == "None":
        query_phone = eval(query_phone)
    if env == "None":
        env = eval(env)
    try:
        if query_phone and env == None:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone,Test_User_Reg.type,
                                       Test_User_Reg.env,Test_User_Reg.description).filter(
                Test_User_Reg.phone.like(query_phone+"%")).all()
        elif query_phone and env:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).filter(
                Test_User_Reg.phone.like(query_phone + "%")).filter_by(env=env).all()
        elif query_phone ==None and env:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).filter_by(env=env).all()
        elif query_phone == None and env ==None:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).all()
        s =map(wc,[telephone for telephone in test_phones])
        msg = {"code":200,"msg":"查询成功","data":s}
    except Exception as e:
        msg = {"code":200,"msg":str(e),"data":"[]"}
    return make_response(jsonify(msg))
def wc(x):
    dictA = {}
    dictA["id"] = x[0]
    dictA["phone"] = x[1]
    dictA["type"] = x[2]
    dictA["env"] = x[3]
    dictA["desc"] = x[4]
    return dictA

@views.route("/query_phone",methods=["GET"])
def query_id():
    """Test_Phones"""
    pid = request.args.get("pid")
    test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).filter_by(id=pid).first()
    msg = {"code":200,"msg":"查询成功","data":test_phones[0]}
    return make_response(jsonify(msg))
@views.route("/update_phone",methods=["GET"])
def update_phone():
    """Test_Phones"""
    pid = request.args.get("pid")
    phone = request.args.get("phone")
    env = request.args.get("env")
    type = request.args.get("type")
    desc = request.args.get("desc")
    try:
        if env not in ["beta", "stage,prod"]:
            raise Exception, "操作环境不存在"
        if len(phone) != 11:
            raise Exception, "手机号需等于11位"
        if type < 0 and type > 6:
            raise Exception, "账号类型说明超出范围"
        if pid =="":
            datas = db.session.query(Test_User_Reg.id).filter_by(phone=phone,type=type,env=env).count()
            if datas != 0:
                raise Exception,"手机号已存在"
            else:
                datas = Test_User_Reg(phone=phone,env=env,type=type,description=desc)
                db.session.add(datas)
        else:
            Test_User_Reg.query.filter_by(id=pid).update(dict(phone=phone,type=type,description=desc,env=env))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))

@views.route("/get_redis_key",methods=["GET"])
def get_redis_key():
    redis_key = db.session.query(Key_Value.user_key).filter_by(status=1).all()
    s = ",".join([key[0] for key in redis_key])
    return s
@views.route("/set_key_value",methods=["GET"])
def set_key_value():
    key = request.args.get("key")
    value = request.args.get("value")
    try:
        if key.upper()=="NONE" or key==None:
            raise Exception,"Key不能为空！"
        redis.set(key,value)
        msg = "set success!"
    except Exception as e:
        print str(e)
        msg = str(e)
    return jsonify({"code":"200","msg":msg})