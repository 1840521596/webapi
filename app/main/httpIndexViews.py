#-*-coding:utf-8 -*-
from . import views
from flask import render_template,request,make_response,jsonify
from .. import db
from ..config.models import Project, Case_Http_API ,Case_Http_File
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
    response = replace_cn(request.form['response'])
    params = replace_cn(request.form["params"])
    headers = replace_cn(request.form["headers"])
    cookies = replace_cn(request.form["cookies"])
    scheduling = request.form["scheduling"]
    assertValue = replace_cn(request.form["assert"])
    islogin = request.form["islogin"]
    account = request.form["account"]
    upload_file = request.form["upload_file"]
    #test_suite = request.form["test_suite"]
    if scheduling == "true":
        scheduling = 1
    else:
        scheduling = 0
    if islogin == "true":
        islogin = 1
    else:
        islogin = 0
    if upload_file == "true":
        upload_file = 1
    else:
        upload_file = 0
    try:
        datas = Case_Http_API(project=project,
                              case_api=case_api,
                              description=case_desc,
                              case_host=case_host,
                              case_url=case_url,
                              method=method,isLogin=islogin,isUpload=upload_file,
                 params=params,response=response,headers=headers,cookies=cookies,
                              scheduling=scheduling,assertValue=assertValue,account=account)
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
    params = replace_cn(request.form['params'])
    response = replace_cn(request.form['response'])
    headers = replace_cn(request.form['headers'])
    cookies = replace_cn(request.form['cookies'])
    scheduling = request.form["scheduling"]
    assertValue = replace_cn(request.form["assert"])
    islogin = request.form["islogin"]
    account = request.form["account"]
    upload_file = request.form["upload_file"]
    if scheduling == "true":
        scheduling = 1
    else:
        scheduling = 0
    if islogin =="true":
        islogin = 1
    else:
        islogin = 0
    if upload_file =="false":
        upload_file = 0
    else:
        upload_file = 1
    try:
        datas = Case_Http_API.query.filter_by(id=pid).update(dict(
            project=project,case_api=case_api,description=description,case_host=case_host,isLogin=islogin,
            case_url=case_url,headers=headers,cookies=cookies,scheduling=scheduling,assertValue=assertValue,
            method=method,params=params,response=response,account=account,isUpload=upload_file))
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
                                  Case_Http_API.assertValue,
                                  Case_Http_API.account,
                                  Case_Http_API.isUpload).filter_by(project=project,case_api=case_api,id=pid,method=method).first()
    resp = {"code": 200, "datas": object_api}
    msg_resp = make_response(jsonify(resp))
    return msg_resp

@views.route("/save_upload_data",methods=["POST"])
def save_upload_data():
    file_1 = request.files['file']
    file_desc = request.form["file_desc"]
    filename = file_1.filename
    content_type = file_1.mimetype
    targetId = request.form["targetId"]  #获取case_api　数据库id值,如接口新建则为999999999
    if targetId=="999999999":  #新建数据
        project = request.form["project"]
        case_api = request.form["case_api"]
        case_desc = request.form["case_desc"]
        case_host = request.form["case_host"]
        case_url = request.form["case_url"]
        method = request.form["method"]
        try:
            targetId = db.session.query(Case_Http_API.id).filter_by(project=project,case_api=case_api,
                                                                description=case_desc,case_host=case_host,
                                                                    case_url=case_url,method=method).first()
            datas = Case_Http_File(case_api_id=str(targetId),file_desc=file_desc,
                                   file_name=filename,content_type=content_type)
            targetId = targetId[0]
            db.session.add(datas)
            db.session.commit()
            resp = {"datas": "%s 更新成功!" % (case_api), "code": 200}
        except Exception as e:
            db.session.rollback()
            resp = {"code": 400, "datas": str(e)}
    else:  #修改数据
        try:
            datas = Case_Http_File.query.filter_by(case_api_id=targetId).update(dict(
                file_desc=file_desc,file_name=filename,content_type=content_type))
            if datas:
                db.session.commit()
                resp = {'datas': '更新成功', 'code': '200'}
            else:  #新增数据
                project = request.form["project"]
                case_api = request.form["case_api"]
                case_desc = request.form["case_desc"]
                case_host = request.form["case_host"]
                case_url = request.form["case_url"]
                method = request.form["method"]
                targetId = db.session.query(Case_Http_API.id).filter_by(project=project, case_api=case_api,
                                                                        description=case_desc, case_host=case_host,
                                                                        case_url=case_url, method=method,
                                                                        id=targetId).first()
                datas = Case_Http_File(case_api_id=targetId[0], file_desc=file_desc,
                                       file_name=filename, content_type=content_type)
                targetId = targetId[0]
                db.session.add(datas)
                db.session.commit()
                resp = {"datas": "%s 更新成功!" % (case_api), "code": 200}
        except Exception as e:
            db.session.rollback()
            resp = {'datas': str(e), 'code': '400'}
    try:
        file_1.save("./app/upload_file/%s_%s" % (targetId,filename))
    except Exception as e:
        resp = {'datas': str(e), 'code': '401'}
    return make_response(jsonify(resp))

def replace_cn(str_params):
    new_str_params = str_params.replace("＂",'"')
    new_str_params1 = new_str_params.replace("＂",'"')
    new_str_params2 = new_str_params1.replace("＇","'")
    new_str_params3 = new_str_params2.replace("，",",")
    new_str_params4 = new_str_params3.replace("｛","{")
    new_str_params5 = new_str_params4.replace("｝","}")
    new_str_params6 = new_str_params5.replace("：",":")
    return new_str_params6
