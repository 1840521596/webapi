#-*-coding:utf-8 -*-
from app.main import test
from flask import request,make_response,jsonify,session,url_for
from app.base.pythonProject.base.getCookies import *
from app.config.project_loginIn import loginIn,replace_cn
import sys
import json
from app.config.sql import betaDB,betaDB_order
import cgi
from collections import OrderedDict
from app.tasks.tasks import run_schedule_api
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
    case_host = request.form["case_host"].strip()
    case_url = request.form["case_url"].strip()
    method = request.form["method"].strip()
    try:
        params = eval(replace_cn(request.form["params"].strip()))
        headers = eval(replace_cn(request.form["headers"].strip()))
        cookies = eval(replace_cn(request.form["cookies"].strip()))
        islogin = request.form["islogin"]
        account_project = request.form["account_project"]
        account_username = request.form["account_username"].strip()
        account_passwd = request.form["account_passwd"].strip()
        url = case_host + case_url
        login_resp_msg = None
        if account_project.upper() == "NONE" or account_project=="":
            account_project = None
        if account_username.upper() == "NONE" or account_username=="":
            account_username = None
        if account_passwd.upper() == "NONE" or account_passwd=="":
            account_passwd = None
        if islogin.upper() == "TRUE" or islogin==True:  #勾选需要登录后获取登录cookies
            login_resp = loginIn(cookies["env_flag"], cookies["env_num"], account_project=account_project ,
                                  account_username=account_username,account_passwd=account_passwd)
            login_resp_code = login_resp["code"]
            login_resp_msg = login_resp["msg"]
            new_cookies = login_resp["cookies"]
            if login_resp_code != 200:
                response = make_response(jsonify({"code": 400, "test_datas": "Login Failed","login_msg": login_resp_msg}))
                return response
            else:
                if method == "POST":
                    resp = postFunction(url, params, headers, new_cookies)
                elif method == "GET":
                    resp = getFunction(url, params, headers, new_cookies)
        else:
            new_cookies = cookies
            if method == "POST":
                resp = postFunction(url, params, headers, new_cookies)
            elif method == "GET":
                resp = getFunction(url, params, headers, new_cookies)
    except Exception as e:
        resp = str(e)
    response = make_response(jsonify({"code":200,"test_datas":cgi.escape(resp),"login_msg":login_resp_msg}))  # 返回response
    return response
@test.route('/doSelfSchedule',methods = ['GET'])
def doSelfSchedule():
    try:
        api_json = request.args.get("api_json")
        schedule_env = request.args.get("schedule_env")
        schedule_num = request.args.get("schedule_num")
        timer = request.args.get("timer")
        api_dict = json.loads(api_json,encoding='utf8')
        orderApiDict = OrderedDict(api_dict.items())    #手工调度接口排序
        cookies = {"env_flag":schedule_env,"env_num":schedule_num}    #cookies
        userName = session['userName']
        origin = "doSelfSchedule"    #来源,异步任务识别操作来源
        task = run_schedule_api.apply_async(args=[origin,orderApiDict,cookies,userName],countdown=int(timer))
        msg = {"code": "200", "msg": "操作成功","id":task.id}
        return jsonify(msg), 202, {'Location': url_for('api_test.taskstatus', task_id=task.id)}
    except Exception as e:
        msg = {"code": "400", "msg": "操作失败","method":"doSelfSchedule","reason": str(e)}
    return make_response(jsonify(msg))
    # run_schedule_api("",origin,orderApiDict,cookies,userName)
    # return make_response(jsonify(orderApiDict))
@test.route('/status/<task_id>')
def taskstatus(task_id):
	task = run_schedule_api.AsyncResult(task_id)
	if task.state == 'PENDING':
		response = {
			'state': task.state,
			'current': 0,
			'total': 1,
			'status': u'启动中...'
		}
	elif task.state != 'FAILURE':
		response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': task.info.get('total', 1),
			'status': task.info.get('status', ''),
			'pass_status':task.info.get('pass_status',''),
			'datas':task.info.get('data_list','')
		}
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info),  # this is the exception raised
			'errorMsg':str(task.traceback)
		}
	return jsonify(response)


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
    order_sn = resp
    sql = """select a.order_id,a.member_id from ysx_order.ysx_order_info a where a.order_sn ="{order_sn}";""".format(order_sn=order_sn)
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
    if phId=="9772" or phId==9772:
        chanel_url = """https://admin.yunshuxie.com/v2/live_course/role/member_role_list.json?memberId=&phone={phone}&sort=memberId&order=asc&limit=10&offset=0&_=1572507705540""".format(phone=phone)
        chanel_resp = requests.get(url=chanel_url,headers=headers,cookies=cookie)
        chanel_resp_dict = json.loads(chanel_resp.text, encoding="utf8")
        moocClassId = chanel_resp_dict["rows"][0]["moocClassId"]
        update_order_sn_sql = """update ysx_order.ysx_wechat_service_user a 
set a.order_sn="{order_sn}"
where a.PHONE="{phone}" and a.MOOC_CLASS_ID="{moocClassId}";""".format(order_sn=order_sn,phone=phone,moocClassId=moocClassId)
        select_data.execute_sql(update_order_sn_sql)
        select_data.execute_close()
    if productCoursehourseId == "9639":
        mzjd_sql = """select a.PRODUCT_COURSE_HOURS_IDS from ysx_order.ysx_order_item a where a.order_id={order_id};""".format(order_id=order_id)
        data = select_data.execute_select(mzjd_sql)
        phids = data[0][0].split(",")
        text = ""
        for phid in range(0,len(phids)-1):
            request_params = {"memberId": member_id, "orderId": order_id, "phone": phone,
                              "productCoursehourseId": phids[phid], "accreditReason": accreditReason}
            resp = requests.post(url=url, data=request_params, headers=headers, cookies=cookie)
            text = resp.text
            resp_dict = json.loads(resp.text, encoding="utf8")
            if resp_dict["returnCode"] == 0 or resp_dict["returnCode"] == "0":
                text += "授权成功,"
            else:
                text +="授权课程请求失败,"
        return text
    else:
        request_params = {"memberId": member_id, "orderId": order_id, "phone": phone,
                          "productCoursehourseId": productCoursehourseId, "accreditReason": accreditReason}
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
    if phId == "9775":
        categoryId = "106"
    else:
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
    phone = request.args.get("phone")
    productId = request.args.get("pId")
    phId = request.args.get("phId")
    product_url = "https://admin.crm.yunshuxie.com/v1/admin/order/query/product_list?productId={productId}&productName=&sort=productId&order=asc&limit=100&offset=0".format(productId=productId)
    cookies = get_ysx_crm_cookie(env_flag="beta",env_num="1")
    resp = requests.get(url=product_url,cookies=cookies)
    productSelect = json.loads(resp.text,encoding="utf-8")
    if productSelect["rows"]:
        for productDict in productSelect["rows"]:
            if int(phId)==productDict["productCourseHoursId"] and int(productId)==productDict["productId"]:
                searchProduct = productDict
                fill_order_params = {"contactPhone": phone, "orderAmount": searchProduct["productPrice"],
                        "productName": searchProduct["productName"],
                        "productId": searchProduct["productId"], "productType": searchProduct["productType"],
                        "courseHoursTitles": searchProduct["courseHoursTitle"],
                        "productCourseHoursId": searchProduct["productCourseHoursId"], "grade": searchProduct["grade"],
                        "originalAmount": searchProduct["productPrice"], "callbackTime": "2019-10-01 00:00:00",
                        "payAccount": "1", "orderSource": "微信", "shareKeyFirst": "-1",
                        "shareKeySecond": "-1","shareKey": "-1", "fromOpenId": "CCrm_653", "chargeTeacher": "赵红玲",
                        "chargeTeacher1": "CCrm_653", "outerTradeId": "osxBJ6MQ69yOMyhCejqj55SdKzyI",
                        "file": file("/home/guohj/Pictures/Operating_System_Apple_Mac_72px_1072593_easyicon.net.png","rb"),
                        "fillOrderDesc": "测试"}

                fill_order_url = "https://admin.crm.yunshuxie.com/fill/order"
                resp = requests.post(url=fill_order_url,data=fill_order_params,cookies=cookies)
                print resp.text

    return make_response(jsonify(resp.text))

