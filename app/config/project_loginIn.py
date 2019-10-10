#!/usr/bin/python
#-*-coding:utf-8 -*-
###_author_:guohongjie
###封装接口测试登录前置
from app.base.pythonProject.base.getCookies import *
def loginIn(project_cn,env_flag,env_num,account):
    """传入测试项目(中文)/测试环境&环境号码/登录账号,返回登录cookies"""
    if project_cn == "云舒写首页":
        new_cookies = get_wacc_home_cookie(env_flag,env_num, account)
    elif project_cn == "云舒写后台管理系统":
        new_cookies = get_wacc_admin_cookie(env_flag,env_num, account)
    elif project_cn == "云舒写CRM系统":
        new_cookies = get_ysx_crm_cookie(env_flag,env_num, account)
    elif project_cn == "简章系统":
        new_cookies = get_wacc_tortoise_cookie(env_flag,env_num, account)
    elif project_cn == "新商品详情系统" or project_cn == "新订单支付系统":
        new_cookies = get_wacc_bird_cookie(env_flag,env_num, account)
    elif project_cn == "罐罐熊APP":
        new_cookies = get_app_cookie(env_flag,env_num, account)
    elif project_cn == "陪你阅读陪你写作":
        new_cookies = get_wechat_cookie(env_flag,env_num, account)
    elif project_cn == "罐罐熊练字课微信小程序":
        new_cookies = get_wechat_ggx_cookies(env_flag,env_num,account)
    elif project_cn == "云舒写大语文合作与推广":
        new_cookies = get_wechat_capth_cookie(env_flag,env_num,account)
    return new_cookies