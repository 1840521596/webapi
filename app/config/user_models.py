#!/usr/bin/python
#-*-coding:utf-8 -*-
from .. import db
from flask_login import UserMixin
class DeptName(UserMixin,db.Model):
    __bind_key__ = 'qa_user'
    __tablename__ = "Dept"  # 部门表
    deptId = db.Column(db.Integer,primary_key=True)#序号ID
    deptName = db.Column(db.String(100)) # 项目
    status = db.Column(db.Boolean,default=0)
    def __init__(self,deptId,deptName,status=0):
        self.deptId = deptId
        self.deptName = deptName
        self.status = status
    def __repr__(self):
        return '<Case %r>'%(self.deptName)