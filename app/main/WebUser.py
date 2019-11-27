#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify
from .. import db,redis
from ..config.models import Project, Case_Http_API,Web_Model_Set,Test_User_Reg,Key_Value
@views.route("/login",methods=["GET"])
def webLogin():
    return render_template('user/login.html')