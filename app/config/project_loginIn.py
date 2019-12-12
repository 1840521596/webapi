#!/usr/bin/python
#-*-coding:utf-8 -*-
###_author_:guohongjie
###封装接口测试登录前置
from app.base.pythonProject.base.getCookies import get_cookies
def loginIn(env_flag,env_num, account_project,
            account_username,account_passwd):
    """传入登录项目(中文)/测试环境&环境号码/登录账号密码,返回登录cookies"""
    new_cookies = get_cookies(account_project,env_flag,env_num,account_username,account_passwd)
    return new_cookies

def replace_cn(str_params):
    """修改全角字符"""
    new_str_params = str_params.replace("＂",'"')
    new_str_params1 = new_str_params.replace("＂",'"')
    new_str_params2 = new_str_params1.replace("＇","'")
    new_str_params3 = new_str_params2.replace("，",",")
    new_str_params4 = new_str_params3.replace("｛","{")
    new_str_params5 = new_str_params4.replace("｝","}")
    new_str_params6 = new_str_params5.replace("：",":")
    return new_str_params6