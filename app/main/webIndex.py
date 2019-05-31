#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify
from .. import db
from ..config.models import Project, Case_Http_API,Web_Model_Set,Test_User_Reg
@views.route("/index",methods=["GET"])
def webIndex():
    """WEB首页"""
    modelNameLink = db.session.query(Web_Model_Set.modelName,Web_Model_Set.modelLink).filter_by(modelStatus=1).order_by("id asc").all()
    modelList = [[m[0],m[1]] for m in modelNameLink]
    print modelList
    projectCount = db.session.query(Project.id).count()
    interfaceCount = db.session.query(Case_Http_API.id).count()
    return render_template('home/index.html', modelNameLink=modelList,project_cout=projectCount,jiekou=interfaceCount)
                           #report=len(reslut_list), project_cout=project_cout,
                         #  model_cout=model_cout, my_tasl=My_task, all_run_case_count=all_run_case_count

@views.route("/testIndex",methods=["GET"])
def testIndex():
    return render_template('home/test_phones.html')

@views.route("/query_phones",methods=["GET"])
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
    type = request.args.get("type")
    desc = request.args.get("desc")
    try:
        Test_User_Reg.query.filter_by(id=pid).update(dict(phone=phone,type=type,description=desc))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
