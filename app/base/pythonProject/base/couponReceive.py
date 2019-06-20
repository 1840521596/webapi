#!/usr/bin/python
#-*-coding:utf-8
from getCookies import get_crm_cookie
import time
import requests
import json
import re
def coupon_test(env_flag,env_num,couponPrice,phone):
    """
    :param couponPrice:   单个代金券价格
    :param phone:   领取手机号码
    :return: log
    """
    resp_log = {}
    session = requests.Session()
    cookies = get_crm_cookie(env_flag,env_num)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1"}
    session.headers = header
    session.cookies = cookies
    date = time.localtime()
    coupon_date = "{}-{:0>2}-{:0>2}".format(date.tm_year,date.tm_mon,date.tm_mday)
    start_date = "{}-{:0>2}-{:0>2} 00:00:00".format(date.tm_year,date.tm_mon,date.tm_mday)
    end_date = "{}-{:0>2}-{:0>2} 23:59:59".format(date.tm_year,date.tm_mon,date.tm_mday)
    url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"
    name = "测试_自动化测试_%d"%(time.time())
    params = {"couponActivityName": name,
              "couponInstructions": "测试_自动化测试创建_%s"%(name),
              "couponTotalAmount": "{}".format(int(couponPrice)*10),
              "couponSingleAmount": "{}".format(couponPrice),
              "couponDailyLimit": "10",
              "limitPersonReceive": "10",
              "activityStartDate": "{}".format(start_date),
              "activityEndDate": "{}".format(end_date),
              "couponType":"1","limitAmount":"","effectiveType": "2",
              "validityDays": "","validatyEndDate": "{}".format(end_date),
              "validatyStartDate": "{}".format(start_date),
              "courseApplyType": "1","courseApply": "-1",
              "sendMode": "2","activityStatus": "","couponActivityId":""}
    #print params
    resp = session.post(url=url,data=params)
    resp_log[u"创建代金券"] = resp.text
    #print "创建代金券:",resp.text
    result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
    assert result["returnCode"]==0 or result["returnCode"]=="0",result["returnMsg"]
    url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list" # 查询代金券 couponActivityId
    params = {"couponActivityName":name,"couponActivityNumber":"","activityStatus":"1","sort":"couponActivityId","order":"DESC","limit":"10","offset":"0"}
    resp = session.get(url=url, params=params)
    resp_log[u"查询代金券"] = resp.text
    print resp.text
    result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
    couponActivityId = result["rows"][0]["couponActivityId"]
    couponActivityNumber = result["rows"][0]["couponActivityNumber"]
    url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  #审核代金券
    params = {"couponActivityId": couponActivityId,"activityStatus": "3"}
    resp = session.post(url=url, data=params)
    resp_log[u"审核代金券"] = resp.text
    #print "审核代金券:",resp.text
    result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
    assert result["returnCode"]==0 or result["returnCode"]=="0",result["returnMsg"]

    url = r"https://pay.yunshuxie.com/v1/coupon/post.htm".format(couponActivityNumber)
    params = {"shareKey": "","actNum": couponActivityNumber,"phone": phone,"code": ""}
    dict_coupins = {}
    coupins = []
    for i in range(10):
        resp = session.post(url,data=params)
        resp_log[u"审核代金券-第%d次"%(i)] = resp.text
        #print "领取代金券:",resp.text
        result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
        assert result["returnCode"] == 48 or result["returnCode"] == "48", result["returnMsg"]
        couponId = "couponId:"+result["data"]["couponId"]
        coupins.append(couponId)
    dict_coupins[u"领取代金券--"+coupon_date] = coupins
    dict_coupins[u"代金券编号"] = couponActivityNumber
    resp_log["coupins_desc"] = dict_coupins
    return resp_log

if __name__ == "__main__":
    print coupon_test(env_flag="beta",env_num="1",couponPrice="20",phone="18519118952")