#-*-coding:utf-8 -*-

from celery import Task,Celery
import time
import requests
backend = "redis://localhost:6379/1"
broker = 'redis://localhost:6379/2'
cel = Celery("test",backend=backend,broker=broker)
class MyTask(Task):
	def on_success(self, retval, task_id, args, kwargs):
		print 'task done: {0}'.format(retval)
		return super(MyTask,self).on_success(retval,task_id,args,kwargs)
	def on_failure(self, exc, task_id, args, kwargs, einfo):
		print 'task fail, reason: {0}'.format(exc)
		return super(MyTask,self).on_failure(exc,task_id,args,kwargs,einfo)

@cel.task(base=MyTask)
def add(url=None):
	url = r"https://admin.yunshuxie.com/v1/SFC/courseManage/getFlowCourseTypeList.htm"
	headers = {"Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded","Cache-Control": "no-cache","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
	cookies = {"env_flag":"beta","env_num":"5"}
	resp = requests.get(url=url,headers=headers,cookies=cookies)
	raise KeyError,'wctv'
	return resp.content
