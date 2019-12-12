#-*-coding:utf-8 -*-
from app.main import views
from flask import render_template,request,make_response,jsonify,session
from app import db
from app.config.api_models import Project
from app.config.user_models import DeptName
@views.route('/projectIndex',methods=['GET','POST'])
def project_select():
    """API测试首页"""
    api_project = Project.query.with_entities(Project.project).distinct().all()
    #提取测试项目,传入页面中
    test_group = DeptName.query.filter(DeptName.status==1).all()
    return render_template("project_edit.html", api_project=api_project,test_groups=test_group)

@views.route('/projectSearch',methods=['GET'])
def project_search():
    project = request.args.get('project')# 项目名称
    test_group = request.args.get('test_group')
    if project=='None' and test_group=='None':
        #当项目为空、接口名为空、状态为 全部
        datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).all()
    elif project=="None" and test_group!='None':
        #项目为空、接口名为空、状态不为all
        datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(test_group=test_group).all()
    elif project!='None' and test_group=='None':
        datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(project=project).all()
    else:
        datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(project=project,test_group=test_group).all()

    resp = {"status": 200, "datas": datas}
    msg_resp = make_response(jsonify(resp))
    return msg_resp

@views.route('/projectInsert',methods=['POST','GET'])
def project_insert():
    """增加测试项目步骤接口"""
    project = request.args.get('project').strip()
    project_en = request.args.get('project_en').strip()
    domain = request.args.get('domain').strip()
    description = request.args.get('description').strip()
    test_group = session["deptName"]
    if project == "" or domain == "" or description == "":
        msg = {"result": "项目名称 or 项目domain or 项目描述 不能为空!"}
    else:
        try:
            datas = Project(project=project,domain=domain,project_en=project_en,description=description,test_group=test_group)
            db.session.add(datas)
            msg = {"status":200,"result":"%s was insert successful!"}
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            msg = {"status": 400,"result":str(e)}
    response = make_response(jsonify(msg)) #返回response
    return response