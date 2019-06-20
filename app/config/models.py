#-*-coding:utf-8 -*-
from .. import db
class Project(db.Model):
    __tablename__ = "project_api"  # 表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    project = db.Column(db.String(100), unique=True) # 项目
    project_en = db.Column(db.String(100), unique=True) # 项目_英文
    domain = db.Column(db.String(100))
    description = db.Column(db.Text)#项目描述
    def __init__(self,project,description,domain,project_en):
        self.project = project
        self.description = description
        self.domain = domain
        self.project_en = project_en
    def __repr__(self):
        return '<Case %r>'%(self.name)


class Case_Http_API(db.Model):
    __tablename__ = "case_http_api" #表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    project = db.Column(db.String(100),db.ForeignKey('project_api.project'))#项目
    case_api = db.Column(db.String(100))#接口名称
    description = db.Column(db.Text)#用例描述
    case_host = db.Column(db.String(500))#请求链接
    case_url = db.Column(db.String(500))#请求链接
    method = db.Column(db.String(10))#请求方式
    params = db.Column(db.Text)#请求参数KEY
    headers = db.Column(db.Text)#请求参数headers
    cookies = db.Column(db.Text)#请求参数cookies
    response = db.Column(db.Text)#预期结果
    status = db.Column(db.Boolean,default=0)
    api_type = db.Column(db.String(5),default='http')
    def __init__(self,project,case_api,params,case_host,headers,cookies,
                 description,case_url,method,response,api_type='http',status=0):
        self.project = project
        self.case_api = case_api
        self.description = description
        self.case_url = case_url
        self.method = method
        self.response = response
        self.status = status
        self.params = params
        self.api_type = api_type
        self.case_host = case_host
        self.headers = headers
        self.cookies = cookies

    def __repr__(self):
        """返回打印数据"""
        return '<Case %r>'%self.project

    def __repr__(self):
        """返回打印数据"""
        return '<Case %r>'%self.project





class Case_Dubbo_API(db.Model):
    __tablename__ = "case_dubbo_api"#表明
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    project = db.Column(db.String(100), db.ForeignKey('project_api.project'))
    host = db.Column(db.String(100))
    port = db.Column(db.Integer)
    name = db.Column(db.String(100))
    case_sys = db.Column(db.String(100))
    serviceName = db.Column(db.String(100))
    methodName = db.Column(db.String(100))
    params = db.Column(db.Text)
    response = db.Column(db.Text)
    status = db.Column(db.Boolean, default=0)
    description = db.Column(db.Text)  # 用例描述
    api_type = db.Column(db.String(5), default='dubbo')
    def __init__(self,project,host,port,name,case_sys,serviceName,methodName,params,response,description,api_type='dubbo',status=0):
        self.project = project
        self.host = host
        self.port = port
        self.name = name
        self.case_sys = case_sys
        self.serviceName = serviceName
        self.methodName = methodName
        self.params = params
        self.response = response
        self.status = status
        self.description = description  # 用例描述
        self.api_type = api_type
    def __repr__(self):
        return '<Case %r>'%(self.name)




class Web_Model_Set(db.Model):
    __tablename__ = "model_set"  # 表明
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    modelName = db.Column(db.String(100))
    modelLink = db.Column(db.String(500))
    modelStatus = db.Column(db.Boolean, default=0)
    def __init__(self,modelName,modelLink,modelStatus):
        self.modelName = modelName
        self.modelLink = modelLink
        self.modelStatus = modelStatus
    def __repr__(self):
        return '<Case %r>'%(self.modelName)


class Test_Env(db.Model):
    __tablename__ = "test_env"  # 表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    env_flag = db.Column(db.String(100)) # 测试环境
    env_num = db.Column(db.String(100))  # 测试环境编号
    def __init__(self,env_flag,env_num):
        self.env_flag = env_flag
        self.env_num = env_num
    def __repr__(self):
        return '<Case %r>'%(self.env_flag)


class Test_User_Reg(db.Model):
    __tablename__ = "telephone"
    id = db.Column(db.Integer,primary_key=True) #序号ID
    phone = db.Column(db.String(11)) #手机号
    type = db.Column(db.Integer,default=0) #注册类型
    env = db.Column(db.String(10)) #环境
    description = db.Column(db.Text) #备注
    def __init__(self,phone,type,env,description=None):
        self.phone = phone
        self.type = type
        self.env = env
        self.description = description
    def __repr__(self):
        return '<Case %r>'%(self.telephone)
