#!/usr/bin/python
#-*-coding:utf-8
html_all = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!-- saved from url=(0104)http://uwsgi.sys.bandubanxie.com/Report/8/9/%E4%BA%91%E8%88%92%E5%86%99CRM%E7%B3%BB%E7%BB%9F_beta_7.html -->
<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>《{project_cn}》--接口测试报告</title>
    <meta name="generator" content="HTMLTestRunner 0.8.2.1">
        <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }
/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>

</head>
<body style="">
<script language="javascript" type="text/javascript">
output_list = Array();
/*level 调整增加只显示通过用例的分类 --Findyou
0:Summary //all hiddenRow
1:Failed  //pt hiddenRow, ft none
2:Pass    //pt none, ft hiddenRow
3:All     //pt none, ft none
*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }
    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}
function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}
function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
<div class="heading">
<h1 style="font-family: Microsoft YaHei">《{project_cn}》--接口测试报告</h1>
<p class="attribute"><strong>测试人员 : </strong> 最棒QA</p>
<p class="attribute"><strong>开始时间 : </strong> {start_time}</p>
<p class="attribute"><strong>结束时间 : </strong> {end_time}</p>
<p class="attribute"><strong>测试结果 : </strong> 共 {case_total}，通过 {case_pass}</p>
<p class="attribute"><strong>测试环境 : </strong> {env_flag}</p>
<p class="attribute"><strong>环境编号 : </strong> {env_num}</p>
<p class="description">云舒写CRM系统</p>
</div>
<p id="show_detail_line">
<a class="btn btn-primary" href="javascript:showCase(0)">概要{ 100.00% }</a>
<a class="btn btn-danger" href="javascript:showCase(1)">失败{ {case_fail} }</a>
<a class="btn btn-success" href="javascript:showCase(2)">通过{ {case_pass} }</a>
<a class="btn btn-info" href="javascript:showCase(3)">所有{ {case_total} }</a>
</p>
<table id="result_table" class="table table-condensed table-bordered table-hover">
<colgroup>
<col align="left">
<col align="right">
<col align="right">
<col align="right">
<col align="right">
<col align="right">
</colgroup>
<tbody><tr id="header_row" class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td style="width:10%">接口名称</td>
    <td style="width:25%">URL</td>
    <td style="width:20%">接口描述</td-->
    <td style="width:5%">请求方式</td>
    <td style="width:20%">请求参数</td>
    <td style="width:20%">详细</td>
</tr>
<tr class="passClass warning">
        {test_case_detailed}
    </tr>
</tbody></table>
</body></html>"""

test_case_detailed = u"""
<tr class="passClass warning">
<td>{api_name}</td>
        <td class="text-center">{api_url}</td>
        <td class="text-center">{description}</td>
        <td class="text-center">{method}</td>
        <td class="text-center"><button id="btn_req_params" type="button" class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target="#btn_req_params_{pid}">详细</button>
            <div id="btn_req_params_{pid}" class="collapse" style="height: 0px;"> 
            <pre>    
        {request_params}
            </pre>
        </div></td>
        <td class="text-center"><button id="btn_resp_json" type="button" class="btn {status_color} btn-xs collapsed" data-toggle="collapse" data-target="#btn_resp_json_{pid}">{case_status}</button>
        <div id="btn_resp_json_{pid}" class="collapse" style="height: 0px;"> 
        <pre>    
        {responce_params}
        </pre>
        </div></td>
</tr>
"""

if __name__ == "__main__":
    api_name = "接口名称"
    api_url = "接口链接"
    request_params = "请求参数"
    assertValue = "校验参数"
    status_color = "btn-success" # or "btn-danger"
    case_status = "通过"
    responce_params = "返回参数"
    method = "GET"
    new_detailed = test_case_detailed.format(api_name=api_name,method=method,api_url=api_url,request_params=request_params,assertValue=assertValue,
                              status_color=status_color,case_status=case_status,responce_params=responce_params)

    project_cn = "测试项目"
    start_time = "20190816"
    end_time = "20190819"
    case_total = "100"
    case_pass = "20"
    env_flag = "beta"
    env_num = "8"
    case_fail = "10"
    wc = html_all.replace("{project_cn}",project_cn)
    wc1 = wc.replace("{test_case_detailed}",new_detailed)
    wc2 = wc1.replace("{start_time}",start_time)
    wc3 = wc2.replace("{end_time}",end_time)
    wc4 = wc3.replace("{case_total}",case_total,2)
    wc5 = wc4.replace("{case_pass}",case_pass,2)
    wc6 = wc5.replace("{env_flag}",env_flag)
    wc7 = wc6.replace("{env_num}",env_num)
    wc8 = wc7.replace("{case_fail}",case_fail)
    with open("C:\Users\Administrator\Desktop\wc.html","w") as f:
        f.write(wc8)