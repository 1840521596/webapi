#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import user
from flask import render_template,request,flash,redirect,url_for,session,g
from flask_login import login_user,logout_user,login_required
from ..config.login_form import LoginForm
from ..config.user_models import User
from app import login_manager
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
def query_user(userid):
    return True
# @user.route("/login",methods=["GET", 'POST'])
# def webLogin():
#     return render_template('user/login.html',form=form)
@user.route("/login",methods=["GET", 'POST'])
def userLogin():
    form = LoginForm()
    if request.method == 'POST':
        print form.accountNumber.data
        print form.password.data
        user = User.query.filter(User.userName == form.accountNumber.data,
                                 User.passwd == form.password.data).first()
        if user:
            login_user(user,remember=True)
            session["userName"] = "guohongjie"
            session["userId"] = "1"
            return redirect(url_for('views.webIndex'))
        else:
            flash(message=u'嗨~{username}!用户名或密码错误!'.format(username=form.accountNumber.data), category='error')
    return render_template('user/login.html',form=form)
@user.route('/logout/')
@login_required
def logout():
    logout_user()  # 登出用户
    return '已经退出登录'
