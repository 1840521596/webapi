#!/usr/bin/env python
#-*-coding:utf-8 -*-
import MySQLdb

def select_sql(sql):
	db = MySQLdb.connect("10.144.24.130","test","test","autoTest",charset='utf8')
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 使用execute方法执行SQL语句
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	cursor.execute("set character_set_server=utf8")
	cursor.execute('SET NAMES UTF8') 
	cursor.execute(sql)
	# 使用 fetchone() 方法获取一条数据
	data = cursor.fetchall()
	# 关闭数据库连接
	db.close()
	return data
def insert_sql(sql):
	db = MySQLdb.connect('10.144.24.130','test','test','autoTest',charset='utf8')
	cursor = db.cursor()
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	cursor.execute("set character_set_server=utf8")
	cursor.execute('SET NAMES UTF8') 
	try:
		cursor.execute(sql)
		db.commit()
		db.close()
		return {"result":True,"reson":"Insert successful"}
	except Exception as e:
		db.rollback()
		db.close()
		return {"result":False,"reson":str(e)}
def update_sql(sql):
	db = MySQLdb.connect('10.144.24.130', 'test', 'test', 'autoTest', charset='utf8')
	cursor = db.cursor()
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	cursor.execute("set character_set_server=utf8")
	cursor.execute('SET NAMES UTF8')
	try:
		cursor.execute(sql)
		db.commit()
		db.close()
		return {"result":True,"reson":"Update successful"}
	except Exception as e:
		db.rollback()
		db.close()
		return {"result":False,"reson":str(e)}

if __name__ == "__main__":
	s = """update behave_config set position='Then 移动鼠标到' where position='Then 移动鼠标';"""
	tupledate = insert_sql(s)
	# ss= """insert into behave_config values('Given 操作页面HTML元素','输入')"""
	# tupledate = insert_sql(ss)
	# sss = """insert into behave_config values('Given 操作页面HTML元素','单击')"""
	# tupledate = insert_sql(sss)
	# ssss = """insert into behave_config values('Then 执行js代码','对弹框操作')"""
	# tupledate = insert_sql(ssss)
	# sssss = """insert into behave_config values('Given 操作页面HTML元素','添加')"""
	# tupledate = insert_sql(sssss)
	# a = """insert into behave_config values('Given 操作页面HTML元素','删除')"""
	# tupledate = insert_sql(a)
	# aa = """insert into behave_config values('Then 移动鼠标','元素区')"""
	# tupledate = insert_sql(aa)
	# aaa= """insert into behave_config values('Then 添加等待时间','秒等待')"""
	# tupledate = insert_sql(aaa)
	#print tupledate
	#print insert_sql(s)


