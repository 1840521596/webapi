#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import user
from flask import render_template,request,flash,redirect,url_for,session,g
from flask_login import login_user,logout_user,login_required
from ..config.login_form import LoginForm
from ..config.user_models import User,DeptName
from app import login_manager
import requests
import json
from .. import db
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
def query_user(userid):
    return True
@user.route("/",methods=["GET", 'POST'])
def webLogin():
    return redirect(url_for('views.webIndex'))
@user.route("/login",methods=["GET", 'POST'])
def userLogin():
    form = LoginForm()
    if request.method == 'POST':
        url = "http://sso.sys.bandubanxie.com/api/v1/auth"
        params = {"Name": form.accountNumber.data, "Password": form.password.data, "IsLdap": "1"}
        resp = requests.post(url=url, data=params)    #SSO登录验证
        dict_resp = json.loads(resp.text, encoding="utf8")
        if resp.status_code==200 and dict_resp["code"]==0:
            session["userName"] = dict_resp.get("data").get("UserInfo").get("Name")
            session["userId"] = dict_resp.get("data").get("UserInfo").get("Id")
            user = User.query.filter(
            User.userName == dict_resp.get("data").get("UserInfo").get("Name")).first()    #查询用户是否存在
            if user:
                dept = DeptName.query.filter(DeptName.deptId == user.deptId).first()    #查询用户部门是否存在
                if not dept:
                    User.deptId = 1    #用户不存在部门时,部门归属为其他
                    db.session.commit()
            else:
                insert_user = User(dict_resp.get("data").get("UserInfo").get("Id"),
                        dict_resp.get("data").get("UserInfo").get("Name"),
                         status=1,
                         deptId=1)
                db.session.add(insert_user)
                db.session.commit()
                user = User.query.filter(
                User.userName == dict_resp.get("data").get("UserInfo").get("Name")).first()  # 查询用户是否存在
            dept = DeptName.query.filter(DeptName.deptId == user.deptId).first()
            session["deptName"] = dept.deptName
            login_user(user, remember=False)
            return redirect(url_for('views.webIndex'))
        else:
            flash(message=u'嗨~{username}!用户名或密码错误!'.format(username=form.accountNumber.data), category='error')
    return render_template('user/login.html',form=form)
@user.route('/logout/')
@login_required
def logout():
    logout_user()  # 登出用户
    session.pop('userName')
    session.pop('deptName')
    session.pop('userId')
    return redirect(url_for('views.webIndex'))
@user.app_errorhandler(404)
def pageNotFound(e):
    return render_template('home/404.html'),404
@user.app_errorhandler(500)
def pageNotFound(e):
    return render_template('home/500.html'),500

