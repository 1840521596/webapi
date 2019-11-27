#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify
from .. import db
from ..config.api_models import Project, Case_Dubbo_API
@views.route('/addDubboProject',methods=['POST','GET'])
def addDubboProject():
    """增加测试项目"""
    if request.method == 'GET':
        projects = db.session.query(Project.project).all()
        msg = {"result":projects}
    elif request.method == 'POST':
        projects = request.form['project']
        descript = request.form['descript']
        try:
            datas = Project(project=projects,description=descript)
            db.session.add(datas)
            db.session.commit()
            msg = {"result": "%s was insert successful!" % (projects)}
        except Exception as e:
            msg = {"result":str(e)}
    response = make_response(jsonify(msg))  # 返回response
    return response
@views.route('/dubboIndex')
def dubbo_select():
    """API测试首页"""
    api_project = Project.query.with_entities(Project.project).distinct().all()
    #提取测试项目,传入页面中
    return render_template("case_dubbo_edit.html", api_project=api_project)
@views.route('/dubboInsert',methods=['POST','GET'])
def dubbo_insert():
    """增加测试用例步骤接口"""
    project = request.form['project']
    host = request.form['host']
    port = request.form['port']
    name = request.form['name']
    case_sys = request.form['case_sys']
    case_service = request.form['case_service']
    case_method = request.form['case_method']
    case_params = request.form["case_params"]
    case_response = request.form["case_response"]
    desc = request.form["desc"]
    try:
        datas = Case_Dubbo_API(project=project,host=host,port=port,
                               name=name,case_sys=case_sys,serviceName=case_service,
                               methodName=case_method,params=case_params,
                               response=case_response,description=desc)
        db.session.add(datas)
        db.session.commit()
        msg = {"result":"%s was insert successful!"%(name)}
    except Exception as e:
        msg = {"result":str(e)}
    response = make_response(jsonify(msg)) #返回response
    return response
@views.route('/dubboSearch',methods=['GET','POST'])
def dubboSearch():
    """接口提供返回测试步骤"""
    project = request.args.get('project')#项目名称
    name = request.args.get('name')
    statu = request.args.get('statu')
    api_name = name if name != "" else False
    if project=='None' and not api_name and statu == 'all':
        #当项目为空、接口名为空、状态为 全部
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).all()
    elif project=='None' and not api_name and statu!='all':
        #项目为空、接口名为空、状态不为all
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
                                status=statu).all()
    elif project=='None' and api_name and statu!="all":
        #项目为空、接口名赋值、状态不为all
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
                                status=statu,name=name).all()
    elif project == 'None' and api_name and statu == "all":
        #项目为空、接口名赋值、状态为all
        datas = db.session.query(Case_Dubbo_API.project, Case_Dubbo_API.host, Case_Dubbo_API.port, Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys, Case_Dubbo_API.serviceName, Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params, Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
             name=name).all()
    elif project != "None" and not api_name and statu=="all":
        #项目不为空、接口名为空、状态为all
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
             project=project).all()
    elif project != "None" and not api_name and statu!="all":
        #项目不为空、接口名为空、状态!=all
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
             status=statu,project=project).all()
    elif project != "None" and api_name and statu in[0,1]:
        #项目不为空、接口名不为空、状态为1 or 2
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
            status=statu, project=project, name=name).all()
    elif project != "None" and api_name and statu =='all':
        #项目不为空、接口名不为空、状态为all
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
            project=project, name=name).all()
    else:
        #剩余为为预期的判断逻辑
        datas = db.session.query(Case_Dubbo_API.project,Case_Dubbo_API.host,Case_Dubbo_API.port,Case_Dubbo_API.name,
                                 Case_Dubbo_API.case_sys,Case_Dubbo_API.serviceName,Case_Dubbo_API.methodName,
                                 Case_Dubbo_API.params,Case_Dubbo_API.response,Case_Dubbo_API.description,
                                 Case_Dubbo_API.status,Case_Dubbo_API.id).filter_by(
            status=statu, project=project, name=name).all()
    resp = {"status": 200, "datas": datas}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@views.route('/dubboUpdate',methods=['GET','POST'])
def dubboUpdate():
    """用例更新操作接口"""
    pid = request.form['pid']
    project = request.form['project']
    host = request.form['host']
    port = request.form['port']
    name = request.form['name']
    case_sys = request.form['case_sys']
    case_service = request.form['case_service']
    case_method = request.form['case_method']
    case_params = request.form["case_params"]
    case_response = request.form["case_response"]
    desc = request.form["desc"]
    try:
        Case_Dubbo_API.query.filter_by(id = pid).update(dict(
                project = project,host = host,port = port,
                name = name,case_sys = case_sys,serviceName = case_service,
                methodName = case_method,params = case_params,
                response = case_response,description = desc))
        db.session.commit()
        resp = {'Msg':'Update was successful','code':'200'}
    except Exception as e:
        resp = {'Msg':str(e),'code':'400'}
    return make_response(jsonify(resp))
@views.route('/dubboDelete')
def dubboDelete():
    """冻结or激活 测试步骤"""
    pid = request.args.get('pid')
    try:
        datas = Case_Dubbo_API.query.filter_by(id=pid).all()
        if datas[0].status:
            Case_Dubbo_API.query.filter_by(id=pid).update({'status':0})
            resp = {'Msg': 'Status was successful', 'code': '200',"status":0}
        else:
            Case_Dubbo_API.query.filter_by(id=pid).update({'status':1})
            resp = {'Msg': 'Status was successful', 'code': '200',"status":1}
        db.session.commit()
    except Exception as e:
        resp = {'Msg':str(e),'code':'400'}
    return make_response(jsonify(resp))
@views.route('/dubboCondition')
def dubboCondition():
    """加载接口名称，操作接口名称配置"""
    project = request.args.get('project')
    object_api = db.session.query(Case_Dubbo_API.name).filter_by(project=project).all()
    dict_resp = {'condition':object_api}
    resp = make_response(jsonify(dict_resp))
    return resp
