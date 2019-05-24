#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ = "guohongjie"
from flask import render_template,request,flash
from . import report
from ..base import report_html
from ..config.config import TEST_FOLDER
@report.route('/Report')
def search_year():
	"""
	测试报告链接
	:return: report.html  测试报告
	"""
	report_path = TEST_FOLDER+"/ReportHtml"
	yearFile = report_html(report_path)
	#print yearFile
	return render_template('report.html',dict_file=yearFile)
@report.route('/Report/<month>/<data>/<html>')
def search_inner(month, data, html):
	"""
	测试完毕后,生成 {date}/{day}/{project}.html,该接口读取Html,并返回至页面
	:param month:  月
	:param data:   日
	:param html:   测试报告
	:return: 测试报告
	"""
	print html
	report_path = TEST_FOLDER + "/ReportHtml" + "/" + month + "/" + data + "/" + html
	html_inner = open(report_path.encode("utf8")).read()
	return html_inner