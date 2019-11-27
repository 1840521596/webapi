#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ ="guohongjie"
from flask import Blueprint
report = Blueprint("main",__name__)  #创建蓝图
test = Blueprint("test",__name__)
views = Blueprint("views",__name__)
mock = Blueprint("mock",__name__)
from . import apiReport,dubbo_views,dubboIndexViews,http_views,httpIndexViews,projectIndexViews,webIndex,\
    http_suite_view,httpSuite,mockServer,WebUser


