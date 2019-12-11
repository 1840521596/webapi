#-*-coding:utf-8 -*-
from app.main import views
from flask import render_template,request,make_response,jsonify
from app import db
from app.config.api_models import Project, Case_Http_API
@views.route('/projectIndex',methods=['GET','POST'])
def project_select():
    """API测试首页"""
    api_project = Project.query.with_entities(Project.project).distinct().all()
    #提取测试项目,传入页面中
    return render_template("project_edit.html", api_project=api_project)

@views.route('/projectSearch',methods=['GET'])
def project_search():
    project = request.args.get('project')# 项目名称
    #print project

    if project=='None':
        #当项目为空、接口名为空、状态为 全部
        datas = db.session.query(Project.id,Project.project,Project.description,Project.domain).all()
    else:
        #项目为空、接口名为空、状态不为all
        datas = db.session.query(Project.id,Project.project,Project.description,Project.domain).filter_by(project=project).all()
    #print datas
    resp = {"status": 200, "datas": datas}
    msg_resp = make_response(jsonify(resp))
    return msg_resp

@views.route('/projectInsert',methods=['POST','GET'])
def project_insert():
    """增加测试用例步骤接口"""
    project = request.args.get('project')
    project_en = request.args.get('project_en')
    domain = request.args.get('domain')
    description = request.args.get('description')

    if project == "" or domain == "" or description == "":
        msg = {"result": "project or domain or description is not null!"}
    else:
        try:
            datas = Project(project=project,domain=domain,project_en=project_en,description=description)
            db.session.add(datas)
            msg = {"status":200,"result":"%s was insert successful!"}
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            msg = {"status": 400,"result":str(e)}
    response = make_response(jsonify(msg)) #返回response
    return response