#-*-coding:utf-8 -*-
from app.main import test
from flask import request,make_response,jsonify
import json
import telnetlib
from telnetlib import Telnet
@test.route('/apiTest/caseDubboLS',methods=['GET'])
def case_dubbo_ls():
    service = []
    if request.method =='GET':
        host = request.args.get('host')
        port = request.args.get('port')
        serviceName = request.args.get('service') or None
        if serviceName:
            command = 'ls %s\n' % (serviceName)
        else:
            command = 'ls\n'
        #以下为telnet链接并发送命令
        telnet = Telnet(host,int(port))# 建立链接
        telnet.write('\n') #点击回车
        telnet.read_until('dubbo>')
        telnet.write(command.encode('utf8'))
        datas = telnet.read_until('dubbo>')
        for m in datas.split('\r'):
            if 'dubbo>' not in m:
                service.append(m.strip(' '))
        return make_response(jsonify({'status':'success','service':service}))
@test.route('/apiTest/caseDubboTest',methods = ['POST','GET'])
def case_dubbo_test():
    result = ''
    new_text = ''
    if request.method == 'POST':
        host = request.form["host"]
        port = request.form["port"]
        service = request.form["service"]
        method = request.form["method"]
        params = request.form["params"]  # data参数
        hope_resp = request.form['response']
    elif request.method == 'GET':
        host = request.args.get("host")
        port = request.args.get("port")
        service = request.args.get("service")
        method = request.args.get("method")
        params = request.args.get("params")  # data参数
    if params == "":
        datas = "None"
    with open('./driver/dubbo/case_dubbo_test.py', 'r') as f:
        api_text = f.read()
    try:
        new_text = api_text.replace('##','').replace('{{HOST}}', host.encode('utf8').strip(' ')
                                   ).replace('{{PORT}}', port.encode('utf8').strip(' ')
                                    ).replace('{{SERVICE_NAME}}', service.encode('utf8').strip(' ')
                                    ).replace('{{METHOD_NAME}}',method.encode('utf8').strip(' ')
                                    ).replace('{{jsonData}}', params.encode('utf8').strip(' '))
        msg=200
        exec(new_text)
    except Exception as e:
        msg = str(e)
    return make_response(jsonify({'resp':result,"testCode":new_text,"msg":msg,'assert_status':"wctv"}))