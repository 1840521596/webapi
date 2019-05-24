#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask import Flask,render_template
from app import create_app,db
from flask_migrate import Migrate
import sys
sys.path.append("./app/base/pythonProject/base")  #添加测试配置路径
app = create_app('default')
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)