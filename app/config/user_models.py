#!/usr/bin/python
#-*-coding:utf-8 -*-
from app import db
from flask_login import UserMixin
class DeptName(db.Model):
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
class User(db.Model,UserMixin):
    __bind_key__ = 'qa_user'
    __tablename__ = "User"  # 部门表
    userId = db.Column(db.Integer,primary_key=True)#序号ID
    userName = db.Column(db.String(100)) # 项目
    status = db.Column(db.Boolean,default=0)
    deptId = db.Column(db.String(100),db.ForeignKey('Dept.deptId'))
    def __init__(self,userId,userName,deptId,status=0):
        self.userId = userId
        self.userName = userName
        self.status = status
        self.deptId = deptId
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.userId)
    def __repr__(self):
        return '<Case %r>'%(self.userName)
# class Dept(db.Model):
#     __bind_key__ = 'qa_user'
#     __tablename__ = "Dept"  # 部门表
#     deptId = db.Column(db.Integer,primary_key=True)#序号ID
#     deptName = db.Column(db.String(100)) # 项目
#     status = db.Column(db.Boolean,default=0)
#     def __init__(self,deptId,deptName,status=0):
#         self.deptId = deptId
#         self.deptName = deptName
#         self.status = status
#     def __repr__(self):
#         return '<Case %r>'%(self.deptName)
