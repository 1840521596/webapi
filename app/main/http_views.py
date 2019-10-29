#-*-coding:utf-8 -*-
from . import test
from flask import request,make_response,jsonify
import requests
from app.base.pythonProject.base.getCookies import *
from .. import db
from ..config.models import Case_Http_File
from ..config.project_loginIn import loginIn
import sys
import json
from app.config.sql import betaDB,betaDB_order
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
@test.route('/case_http_test',methods = ['POST'])
def case_http_test():
    """
    :param case_host:  domain
    :param case_url:  path
    :param method:  请求方式
    :return:  Response
    """
    project_cn = request.form["project_cn"]
    case_host = request.form["case_host"]
    case_url = request.form["case_url"]
    method = request.form["method"]
    try:
        params = eval(request.form["params"])
        headers = eval(request.form["headers"])
        cookies = eval(request.form["cookies"])
        islogin = request.form["islogin"]
        projectAccount = request.form["account"]
        account_list = projectAccount.split("&")
        if len(account_list)==1:    #登录账号进行分割,当不存在"测试使用"测试项目前置时,直接使用账号
            account = account_list[0]
            test_use = None
        else:
            test_use,account = account_list[0],account_list[1]    #测试项目&测试账号
        url = case_host + case_url
        isUpload = request.form["isUpload"]
        targetId = request.form["pid"]
        if account.upper() == "NONE" or account==None:
            account = None
        if islogin.upper() == "TRUE" or islogin==True:  #勾选需要登录后获取登录cookies
            new_cookies = loginIn(project_cn,cookies["env_flag"], cookies["env_num"], account,test_use)
            if case_url in ["/auth/loginCheck"]:
                params = {}
                params["sessionId"] = new_cookies["sso_sessionid"]
            if case_url in ["/auth/logout"]:
                params["sessionId"] = new_cookies["sso_sessionid"]
        else:
            new_cookies = cookies
        if isUpload=="false":  #不需要上传文件
            if method=="POST":
                resp = postFunction(url,params,headers,new_cookies)
            elif method=="GET":
                resp = getFunction(url,params,headers,new_cookies)
        else:  #已上传文件,进入界面点击测试
            file_name = db.session.query(Case_Http_File.file_name,
                                         Case_Http_File.content_type,
                                         Case_Http_File.file_desc,
                                         Case_Http_File.case_api_id).filter_by(case_api_id=targetId).first()
            if file_name:
                file_1 = open("./app/upload_file/%s_%s"%(file_name[3],file_name[0]))
                upload_file = {file_name[2]: (file_name[0], file_1, file_name[1])}
                if method=="POST":
                    resp = postFunctionFile(url,params,headers,new_cookies,upload_file)
                elif method=="GET":
                    resp = getFunctionFile(url,params,headers,new_cookies,upload_file)
            else:
                raise Exception,"当前接口未存在测试文件,请重新上传后测试！"
        if project_cn == u"CRM绩效规则重构":
            resp_dict = json.loads(resp, encoding="utf8")
            if resp_dict["returnCode"] != "0" and resp_dict["returnCode"] != 0:
                resp = resp_dict["returnMsg"]
            else:
                try:
                    if case_url == "/v6/order/face_course/post/create_order.htm":
                        order_sn = update_order_status(resp)
                        resp = order_sn
                    else:
                        phone = params["phone"]
                        phId = params["phId"]
                        pId = params["pId"]
                        order_sn = update_order_status(resp)  #更改订单状态=2,call_back＝当前时间,返回order_sn　字段
                        if pId in ["7698","8326","8327","8215","7996"]:    #罐罐熊正式课&练字课商品ID,并对应授权
                            msg = bearJoinCategoryProduct(phone,phId,cookies,order_sn)
                        else:
                            msg = joinCategoryProduct(phone,phId,cookies,order_sn)    #传入order_sn字段,查找　memberId,orderId

                        resp = order_sn + ":" + msg
                except Exception as e:
                    resp = str(e)
    except Exception as e:
        resp = str(e)
    response = make_response(jsonify({"code":200,"datas":resp}))  # 返回response
    return response



def postFunction(url,params,headers,cookies):
    resp = requests.post(url,data=params,headers=headers,cookies=cookies)
    return resp.content
def getFunction(url,params,headers,cookies):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies)
    return resp.content
def postFunctionFile(url,params,headers,cookies,file):
    resp = requests.post(url,data=params,headers=headers,cookies=cookies,files=file)
    return resp.content
def getFunctionFile(url,params,headers,cookies,file):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies,files=file)
    return resp.content

@test.route("/test_upload",methods=["POST"])
def upload_test():
    project_cn = request.form["project_cn"]
    case_host = request.form["case_host"]
    case_url = request.form["case_url"]
    method = request.form["method"]
    file_desc = request.form["file_desc"]
    try:
        params = eval(request.form["params"])
        headers = eval(request.form["headers"])
        cookies = eval(request.form["cookies"])
        islogin = request.form["islogin"]
        account = request.form["account"]
        file_1 = request.files['file']
        upload_file = {file_desc:(file_1.filename, file_1, file_1.mimetype)}
        url = case_host + case_url
        if account.upper() == "NONE" or account == None:
            account = None
        if islogin.upper() == "TRUE" or islogin == True:
            new_cookies = loginIn(project_cn,cookies["env_flag"], cookies["env_num"], account).get_dict()
        else:
            new_cookies = cookies
        if method == "POST":
            resp = postFunctionFile(url, params, headers, new_cookies,upload_file)
        elif method == "GET":
            resp = getFunctionFile(url, params, headers, new_cookies,upload_file)
    except Exception as e:
        resp = str(e)
    response = make_response(jsonify({"code": 200, "datas": resp}))  # 返回response
    return response


def update_order_status(resp):
    select_data = betaDB()
    resp_dict = json.loads(resp, encoding="utf8")
    outTradeNo = resp_dict["data"]["outTradeNo"]
    sql = """update ysx_order.ysx_order_info a  set a.order_state="2" , a.callback_time= now(),a.ORDER_AMOUNT='100',a.ORIGINAL_AMOUNT='100' where a.order_sn ="{order_sn}";""".format(
    order_sn=outTradeNo)
    select_data.execute_sql(sql)
    select_data.execute_close()
    resp = outTradeNo
    return resp
def joinCategoryProduct(phone,phId,cookies,resp):
    select_data = betaDB()
    sql = """select a.order_id,a.member_id from ysx_order.ysx_order_info a where a.order_sn ="{order_sn}";""".format(order_sn=resp)
    data = select_data.execute_select(sql)
    order_id,member_id = data[0][0],data[0][1]
    phone = phone
    productCoursehourseId = phId
    accreditReason = u"测试使用"
    url = r"https://admin.yunshuxie.com/v1/admin/write_source/writeCourse/joinCategoryProduct.json"
    cookie = get_wacc_admin_cookie(env_flag=cookies["env_flag"],env_num=cookies["env_num"]).get_dict()
    request_params = {"memberId":member_id,"orderId":order_id,"phone":phone,
                      "productCoursehourseId":productCoursehourseId,"accreditReason":accreditReason}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    resp = requests.post(url=url,data=request_params,headers=headers,cookies=cookie)
    resp_dict = json.loads(resp.text,encoding="utf8")
    if resp_dict["returnCode"] == 0 or resp_dict["returnCode"] == "0":
        return "授权成功"
    else:
        return "授权课程请求失败"
def bearJoinCategoryProduct(phone,phId,cookies,resp):
    select_data = betaDB()
    sql = """select a.order_id,a.member_id from ysx_order.ysx_order_info a where a.order_sn ="{order_sn}";""".format(order_sn=resp)
    data = select_data.execute_select(sql)
    order_id,member_id = data[0][0],data[0][1]
    phone = phone
    productCoursehourseId = phId
    accreditReason = u"测试使用"
    categoryId = "102"
    grade = "1"
    url = r"https://admin.yunshuxie.com/v1/elementary/joinCategoryProduct.json"
    cookie = get_wacc_admin_cookie(env_flag=cookies["env_flag"],env_num=cookies["env_num"]).get_dict()
    request_params = {"memberId":member_id,"orderId":order_id,"phone":phone,"categoryId":categoryId,"grade":grade,
                      "productCoursehourseId":productCoursehourseId,"accreditReason":accreditReason}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    resp = requests.post(url=url,data=request_params,headers=headers,cookies=cookie)
    resp_dict = json.loads(resp.text,encoding="utf8")
    if resp_dict["returnCode"] == 0 or resp_dict["returnCode"] == "0":
        return "授权成功"
    else:
        return "授权课程请求失败"


@test.route("/test_protected",methods=["GET"])
def test_protected():
    """30保护期校验"""
    tiyan_order_sn = request.args.get("tiyan_order_sn")
    zhengshi_order_sn = request.args.get("zhengshi_order_sn")
    isProtected = request.args.get("isProjected")
    courser_day = """SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
                 INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
                 INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
                 INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
                 INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
                 WHERE yoyoi.order_sn = "{tiyan_order_sn}" ;""".format(
        tiyan_order_sn=tiyan_order_sn)
    select_datas = betaDB_order()
    COURSE_START_DATE = select_datas.execute_select(courser_day)[0][0]
    if isProtected =="0":    #需要保护期外数据
        sql = """select timestampdiff(day,
    (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
     INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
     INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
     INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
     INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
     WHERE yoyoi.order_sn = "{tiyan_order_sn}")/*体验课程开始时间*/,
    (select a.CALLBACK_TIME from ysx_order.ysx_order_info a where a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2')/*正式课程下单时间*/
    )""".format(tiyan_order_sn=tiyan_order_sn,zhengshi_order_sn=zhengshi_order_sn)
        data = select_datas.execute_select(sql)[0][0]
        if data>30:
            min_data_sql = """select callback_time from ysx_order.YSX_ORDER_INFO where order_sn="{zhengshi_order_sn}" and order_state="2";""".format(zhengshi_order_sn=zhengshi_order_sn)
            min_data = select_datas.execute_select(min_data_sql)[0][0]
            datas = "%s:保护期外,不做处理"%(min_data)
        else:
            add_30_days = """
            select date_add(
    (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
     INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
     INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
     INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
     INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
     WHERE yoyoi.order_sn = "{tiyan_order_sn}" ),interval 31 day) from dual;""".format(tiyan_order_sn=tiyan_order_sn)
            data = select_datas.execute_select(add_30_days)[0][0]
            update_sql = """update ysx_order.ysx_order_info a set a.callback_time='{tdate}' where
      a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2';""".format(tdate=data,zhengshi_order_sn=zhengshi_order_sn)
            update_data = betaDB()
            update_data.execute_sql(update_sql)
            update_data.execute_close()
            datas="%s:保护期外+30天完成增加"%(data)
    else:    #需要保护期内数据
        sql = """select timestampdiff(day,
            (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
             INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
             INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
             INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
             INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
             WHERE yoyoi.order_sn = "{tiyan_order_sn}")/*体验课程开始时间*/,
            (select a.CALLBACK_TIME from ysx_order.ysx_order_info a where a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2')/*正式课程下单时间*/
            )""".format(tiyan_order_sn=tiyan_order_sn, zhengshi_order_sn=zhengshi_order_sn)
        data = select_datas.execute_select(sql)
        if data < 30:
            min_data_sql = """select callback_time from ysx_order.YSX_ORDER_INFO where order_sn="{zhengshi_order_sn}" and order_state="2";""".format(
                zhengshi_order_sn=zhengshi_order_sn)
            min_data = select_datas.execute_select(min_data_sql)[0][0]
            datas = "%s:保护期内,不做处理" % (min_data)
        else:
            add_29_days = """
                    select date_add(
            (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
             INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
             INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
             INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
             INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
             WHERE yoyoi.order_sn = "{tiyan_order_sn}" ),interval 29 day) from dual;""".format(
                tiyan_order_sn=tiyan_order_sn)
            COURSE_START_DATE =select_datas.execute_select(courser_day)[0][0]
            data = select_datas.execute_select(add_29_days)[0][0]
            update_sql = """update ysx_order.ysx_order_info a set a.callback_time='{tdate}' where
              a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2';""".format(tdate=data,
                                                                                zhengshi_order_sn=zhengshi_order_sn)
            update_data = betaDB()
            update_data.execute_sql(update_sql)
            update_data.execute_close()
            datas = "%s:保护期内+课程开课事件增加29天完成"%(data)
    select_datas.execute_close()
    response = make_response(jsonify({"code": 200,"COURSE_START_DATE":str(COURSE_START_DATE) ,"CALLBACK_TIME": datas}))  # 返回response
    return response
@test.route("/test_fill_order",methods=["GET"])
def test_file_order():
    """接口生成补单"""
    productId = request.args.get("pId")
    product_url = "https://admin.crm.yunshuxie.com/v1/admin/order/query/product_list?productId={productId}&productName=&sort=productId&order=asc&limit=100&offset=0".format(productId=productId)
    cookies = get_ysx_crm_cookie(env_flag="beta",env_num="1")
    resp = requests.get(url=product_url,cookies=cookies)
    print resp
    fill_order_url = "https://admin.crm.yunshuxie.com/fill/order"
    return make_response(jsonify(resp.text))

