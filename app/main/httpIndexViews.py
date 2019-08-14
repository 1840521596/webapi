#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify
from .. import db
from ..config.models import Project, Case_Http_API
@views.route('/addHttpProject',methods=['POST','GET'])
def add_project():
    """增加测试项目"""
    if request.method == 'GET':
        projects = db.session.query(Project.project).all()
        msg = {"datas":projects,"code":200}
    elif request.method == 'POST':
        projects = request.form['project']
        descript = request.form['descript']
        try:
            datas = Project(project=projects,description=descript)
            db.session.add(datas)
            db.session.commit()
            msg = {"datas": "%s was insert successful!" % (projects),"code":200}
        except Exception as e:
            msg = {"datas":str(e),"code":200}
    response = make_response(jsonify(msg))  # 返回response
    return response
@views.route('/httpIndex')
def http_select():
    """API测试首页"""
    api_project = Case_Http_API.query.with_entities(Project.project).distinct().all()
    #提取测试项目,传入页面中
    return render_template("case_http_edit.html", api_project=api_project)
@views.route('/httpInsert',methods=['POST'])
def http_insert():
    """增加测试用例步骤接口"""
    project = request.form['project']
    case_api = request.form['case_api']
    case_desc = request.form['description']
    case_host = request.form['case_host']
    case_url = request.form['case_url']
    method = request.form['method']
    response = request.form['response']
    params = request.form["params"]
    headers = request.form["headers"]
    cookies = request.form["cookies"]
    scheduling = request.form["scheduling"]
    assertValue = request.form["assert"]
    islogin = request.form["islogin"]
    if scheduling == "true":
        scheduling = 1
    else:
        scheduling = 0
    if islogin == "true":
        islogin = 1
    else:
        islogin = 0
    try:
        datas = Case_Http_API(project=project,
                              case_api=case_api,
                              description=case_desc,
                              case_host=case_host,
                              case_url=case_url,
                              method=method,isLogin=islogin,
                 params=params,response=response,headers=headers,cookies=cookies,scheduling=scheduling,assertValue=assertValue)
        db.session.add(datas)
        db.session.commit()
        msg = {"datas":"%s 更新成功!"%(case_api),"code":200}
    except Exception as e:
        db.session.rollback()
        msg = {"code":400,"datas":str(e)}
    response = make_response(jsonify(msg)) #返回response
    return response
@views.route('/httpSearch',methods=['GET'])
def search():
    """接口提供返回测试步骤"""
    project = request.args.get('project')#项目名称
    name = request.args.get('name')
    statu = request.args.get('statu')
    api_name = name if name != " " else False
    if project=='None' and not api_name and statu == 'all':
        #当项目为空、接口名为空、状态为 全部
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).all()
    elif project=='None' and not api_name and statu != 'all':
        #项目为空、接口名为空、状态不为all
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(
                                status=statu).all()
    elif project=='None' and api_name and statu == 'all':
        #项目为空、接口名赋值、状态为all
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(
                                case_api=name).all()
    elif project=='None' and api_name and statu != 'all':
        #项目为空、接口名赋值、状态不为all
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(
                                case_api=name,status=statu).all()
    elif project != "None" and not api_name and statu == 'all':
        #项目不为空、接口名为空、状态不为all
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(project=project).all()
    elif project != "None" and not api_name and statu != 'all':
        #项目不为空、接口名为空、状态不为all
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(project=project,status=statu).all()
    elif project != "None" and api_name and statu == 'all':
        #项目不为空、接口名不为空、状态为1,2
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(project=project, case_api=name).all()
    elif project != "None" and api_name and statu != 'all':
        #项目不为空、接口名不为空、状态为1,2
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(
        project=project, case_api=name,status=statu).all()
    else:
        #剩余为为预期的判断逻辑
        datas = db.session.query(Case_Http_API.id,Case_Http_API.project,Case_Http_API.case_api,Case_Http_API.description,Case_Http_API.case_url,Case_Http_API.method,
                                 Case_Http_API.params,Case_Http_API.response,Case_Http_API.status).filter_by(
                                project=project, case_api=name).all()
    resp = {"code": 200, "datas": datas}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@views.route('/httpUpdate',methods=['GET','POST'])
def update():
    """用例更新操作接口"""
    pid = request.form['pid']
    project = request.form['project']
    case_api = request.form['case_api']
    description = request.form['description']
    case_host = request.form['case_host']
    case_url = request.form['case_url']
    method = request.form['method']
    params = request.form['params']
    response = request.form['response']
    headers = request.form['headers']
    cookies = request.form['cookies']
    scheduling = request.form["scheduling"]
    assertValue = request.form["assert"]
    islogin = request.form["islogin"]

    if scheduling == "true":
        scheduling = 1
    else:
        scheduling = 0
    if islogin =="true":
        islogin = 1
    else:
        islogin = 0
    try:
        Case_Http_API.query.filter_by(id=pid).update(dict(
            project=project,case_api=case_api,description=description,case_host=case_host,isLogin=islogin,
            case_url=case_url,headers=headers,cookies=cookies,scheduling=scheduling,assertValue=assertValue,
            method=method,params=params,response=response))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route('/httpDelete',methods=["GET"])
def delete():
    """删除测试步骤"""
    pid = request.args.get("pid")
    status = request.args.get("status")
    try:
        Case_Http_API.query.filter_by(id=pid).update(dict(status=int(status)))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        print str(e)
        resp = {"code": 400, "datas": str(e)}
    return make_response(jsonify(resp))

@views.route('/httpCondition')
def case_condition():
    """加载接口名称，操作接口名称配置"""
    project = request.args.get('project')
    object_api = db.session.query(Case_Http_API.case_api).filter_by(project=project).all()
    dict_resp = {"code": 200, "datas":object_api}
    resp = make_response(jsonify(dict_resp))
    return resp

@views.route("/httpUnionSearch",methods=['GET'])
def httpUnionSearch():
    project = request.args.get('project')
    case_api = request.args.get('case_api')
    pid = request.args.get('pid')
    method = request.args.get('method')
    object_api = db.session.query(Case_Http_API.project,
                                  Case_Http_API.case_api,
                                  Case_Http_API.description,
                                  Case_Http_API.case_host,
                                  Case_Http_API.case_url,
                                  Case_Http_API.method,
                                  Case_Http_API.response,
                                  Case_Http_API.params,
                                  Case_Http_API.headers,
                                  Case_Http_API.cookies,
                                  Case_Http_API.scheduling,
                                  Case_Http_API.isLogin,
                                  Case_Http_API.assertValue).filter_by(project=project,case_api=case_api,id=pid,method=method).first()
    resp = {"code": 200, "datas": object_api}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
