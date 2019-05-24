#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify
from .. import db
from ..config.models import Project, Case_Http_API,Web_Model_Set
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
