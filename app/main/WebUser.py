#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import user
from flask import render_template,request,make_response,jsonify,flash,redirect,url_for
from flask_login import UserMixin,login_user
from ..config.user_models import DeptName
from .. import db
from .webIndex import webIndex
from app import login_manager
def query_user(user_id):
    return True
@user.route("/login",methods=["GET", 'POST'])
def webLogin():
    return render_template('user/login.html')
@user.route("/userLogin",methods=["GET", 'POST'])
def userLogin():
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Access denied.'
    if request.method == 'GET':
        user_id = 2#request.form.get('userid')
        user = query_user(user_id)
        if user is not None:
            curr_user = DeptName(1,1)
            curr_user.id = user_id
            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)
            return redirect(url_for('views.webIndex'))
        flash('Wrong username or password!')
    # GET 请求
    return render_template('home/index.html')