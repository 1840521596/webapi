var get_title="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" width=\"20%\" class=\"wctv\">Params(参数）</th>\n" +
    "       <th colspan=\"3\" width=\"20%\" class=\"wctv\">Headers(标头)</th>\n" +
    "       <th colspan=\"2\" width=\"20%\" class=\"wctv\">Cookies(缓存)</th>\n" +
    "      </tr>";
var get_data="<tr height=\"36px\">\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_params\" placeholder=\"测试数据\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='测试数据'\"></td>\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_headers\" placeholder=\"Headers\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Headers'\"></td>\n" +
    "<td colspan=\"2\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_cookies\" placeholder=\"Cookies\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Cookies'\"></td>\n" +
    "</tr>"


var post_title="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" width=\"20%\" style=\"text-align:center;\"  class=\"wctv\">Data(参数）</th>\n" +
    "       <th colspan=\"3\" width=\"20%\" style=\"text-align:center;\" class=\"wctv\">Headers(标头)</th>\n" +
    "       <th colspan=\"2\" width=\"15%\" style=\"text-align:center;\" class=\"wctv\">Cookies(缓存)</th>\n" +
    "      </tr>";

var post_data="<tr height=\"36px\">\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_params\" placeholder=\"测试数据\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='测试数据'\"></td>\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_headers\" placeholder=\"Headers\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Headers'\"></td>\n" +
    "<td colspan=\"2\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_cookies\" placeholder=\"Cookies\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Cookies'\"/></td>\n" +
    "</tr>"

var file_data ="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" style=\"text-align:center;\">file_desc(备注）</th>\n" +
    "       <th colspan=\"5\" style=\"text-align:center;\" >上传文件</th>\n" +
        "<tr height=\"36px\">\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"file\" id=\"file_desc\" placeholder=\"file_desc\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='file_desc'\"></td>\n" +
        "<td colspan=\"2\" class=\"wctv\"><input style=\"width: 100%; height: 100%\" type=\"file\" id=\"FileUpload\" placeholder=\"FileUpload\" name=\"FileUpload\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='FileUpload'\"></td>\n" +
        "<td colspan=\"2\" class=\"wctv\"><button class=\"btn btn-default\" onclick=\"btn_upload()\">上传</button><button class=\"btn btn-default\" onclick=\"btn_clear()\">清空</button></td>\n" +
    "</tr>"





$("#btn2").click(function () {
        $.ajax({
            url: "/httpSearch",
            type: "get",
            data: {
                project: $("#project").find("option:selected").val(),
                name: $("#case_name").val(),
                statu: $("#state").find("option:selected").val()
            }
        }).done(function (result) {
            var _temo = []
            for (var i = 0; i < result['datas'].length; i++) {
                _temo.push(result['datas'][i]);
            }
            var tableHTML = ""
            for (var i = 0; i < _temo.length; i++) {
                var j = i + 1;
                //alert(_temo[i]);
                if (_temo[i][8]==false){
                tableHTML = tableHTML + '<tr><td id="pid" style="display:none">' + _temo[i][0] + '</td><td >' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td><td>' + _temo[i][4] + '</td><td>' + _temo[i][5] + '</td><td style="display:none">' + _temo[i][6] + '</td><td style="display:none">' + _temo[i][7] + '</td><td style="display:none">'+ _temo[i][8] + '</td><td style="text-align: center;"><a data-pid="' + _temo[i][0] + '"class="btn btn-primary btn-large update">修改</a>&nbsp&nbsp&nbsp&nbsp<a data-pid="0"class="btn btn-primary btn-large  delet">激活</a></td></tr>'}
                else{
                    tableHTML = tableHTML + '<tr><td id="pid" style="display:none">' + _temo[i][0] + '</td><td >' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td><td>' + _temo[i][4] + '</td><td>' + _temo[i][5] + '</td><td style="display:none">' + _temo[i][6] + '</td><td style="display:none">' + _temo[i][7] + '</td><td style="display:none">'+ _temo[i][8] + '</td><td style="text-align: center;"><a data-pid="' + _temo[i][0] + '"class="btn btn-primary btn-large update">修改</a>&nbsp&nbsp&nbsp&nbsp<a data-pid="1"class="btn btn-primary btn-large  delet">冻结</a></td></tr>'
                }}//case_name+description+case_url+method+parameter+assert
            $("#casetb").html(tableHTML);
        })
    })

//获取 select=使用 的option
var func = function () {
        $.ajax({
        url: "/condition",
        type: "get",
        data: {
            project: $("#project option:selected").text()
        }
    }).done(function (result) {
        var selectHTML = ""
        for (var i = 0; i < result.condition.length; i++) {
            selectHTML = selectHTML + '<option value="">' + result.condition[i] + '</option>'
        }
        $("#api_name").html(selectHTML);
    })
}

jQuery(document).ready(function ($) {
    $('.theme-login').click(function () {
        $('.theme-popover-mask').fadeIn(100);
        $("#RS").html("");
        $("#RC").html("");
        $("#project_choice").val("");
        $("#targetId").val(999999999)
        $("#case_api").val("");
        $("#case_desc").val("");
        $("#case_url").val("");
        $("#method").val("");
        $("#key").val("");
        $("#except_result").val("");
        //$("#btn4").css("display","none");
        $("#actual_result").val("");
        $("#actual_result").attr("readOnly","true");
        $("#actual_result").removeAttr("style");
        $('.theme-popover').slideDown(200);
        $("#btn4").bind("click",http_test);
    })
    $('.theme-poptit .close').click(function () {
        $('.theme-popover-mask').fadeOut(100);
        $('.theme-popover').slideUp(200, function () {
            var _td = $("#tbdata").find("td");
            $("#btn4").unbind("click");
            $("#btn6").unbind("click");
            $("#btn7").unbind("click");
        });
       // $("#targetId").val("");
        //alert("关闭");
        //location.reload();
    });
//    $("body").delegate(".run", "click", function () {
//        var _this = $(this);
//        if ($("#casetb td").length && $("#casetb td").length !== 0) {
//        	if(_this.hasClass("active")){
//        	   alert("用例正在执行请稍后操作！")
//               return;
//            }else{
//                var brow = $("#casefeature td").eq(2).find("option:selected").text()
//                $.ajax({
//                    url: "http:/uwsgi.sys.bandubanxie.com:5000/search_docker",
//                    type: "get",
//                    data: {
//                        browser:brow
//                    },
//                    success:function(data){
//                        if (data.url == "null") {
//                            alert(data.msg);
//                            return;
//                        }else{
//                            caseRun(data.url);
//                            _this.addClass("active");
//                        }
//                    }
//                })
//            }
//        } else {
//            alert("无用例数据！");
//        }
//    });
    function caseRun(urldata){
        var brow = $("#casefeature td").eq(2).find("option:selected").text()
        var step = [];
        var run_case = [];
        $("#casetb tr").each(function () {
            var tr = $(this);
            step.push([
                tr.find("td").eq(1).text(),
                tr.find("td").eq(2).text(),
                tr.find("td").eq(3).text(),
                tr.find("td").eq(4).text()
            ]);
            for (var i = 0; i < step.length; i++) {
                run_case[i] = step[i]
            }
        });
        var email = "";
        var emailmatch = "";
        if ($("#emailadrr").val() !== "") {
            emailmatch = $("#emailadrr").val(); 
            if(!emailmatch.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/))
              {
                alert("格式不正确！请重新输入");
                $("#emailadrr").focus();
                return;
              }else{
                email = $("#emailadrr").val();
              }
        }
        $.ajax({
            url: urldata + "/case_run",
            type: "post",
            data: {
                brow: brow,
                case: JSON.stringify(run_case),
                url: urldata,
                email: email
            }
        });
        var loopfn = function () {
            $.ajax({
                url: urldata + "/re_status",
                type: "get",
                success: function (data) {
                    if (data.result == "end_step") {
                        var msg = "是否自动刷新页面？";
                        if (confirm(msg) == true) {
                            window.location.reload();
                        }
                    } else {
                        $('.theme-popover-mask').fadeIn(100);
                        $('.theme-popover').html("");
                        $('.theme-popover').attr("style", "width:80%");
                        //$('.theme-popover').attr("style","left:20%");
                        var imgli = '<img src="'+urldata+'/re_images/' + data.images + '" style="margin-top: -8%;margin-left: 0%;width: 100%;height: 900px;"></img>'
                        $('.theme-popover').append($(imgli));
                        $('.theme-popover').slideDown(200);
                        setTimeout(loopfn, 1000);
                    }
                }
            })
        }
        loopfn()
    }


    function changeTheme(data,api_pid) {
        $("#RS").html("");
        $("#RC").html("");
        $("#actual_result").val("");
        $("#actual_result").removeAttr("style");
        $("#btn4").removeAttr("style");
        var _td = $("#tbdata").find("td");
        var _td_1 =  $("#tbdata_1").find("td");
       // alert(api_pid);
        $("#targetId").val(api_pid);
        //alert(_td.eq(0));
        _td.eq(1).find("option").attr("selected",false);
        _td.eq(1).find("option[value="+data[0]+"]").prop("selected",true);
        _td.eq(2).find("input").val(data[1]);
        _td.eq(3).find("input").val(data[2]);
        _td.eq(4).find("input").val(data[3]);
        _td.eq(5).find("input").val(data[4]);
        _td.eq(6).find("option").attr("selected",false);
        _td.eq(6).find("option[value="+data[5]+"]").prop("selected",true);
        _td.eq(7).find("input").val(data[6]);
        document.getElementById("check1").checked=data[10];
        //alert(data[14]);
        document.getElementById("check3").checked=data[14];
        if (data[10]){
        $("#assert").attr('disabled',false);
        //$("#test_suite").attr('disabled',false);
        }
        else{
        $("#assert").attr('disabled',true);
        //$("#test_suite").attr('disabled',true);
        }
        document.getElementById("check2").checked=data[11];
        if (data[11]){
        $("#account").attr('disabled',false);
        }
        else{
        $("#account").attr('disabled',true);
        }
        document.getElementById("assert").value=data[12];
        document.getElementById("account").value=data[13];  //account
       // document.getElementById("test_suite").value=data[14];  //test_suite
        var _ad = $("#apt_datas").find("td");
        //alert(data[0]);
        if (data[5]=='GET'){
            //alert(_ad.eq(0));
            _ad.eq(0).find("input").val(data[7]);
            _ad.eq(1).find("input").val(data[8]);
            _ad.eq(2).find("input").val(data[9]);
        }
        else if(data[5]=='POST'){
            //alert(_ad.eq(0));
            _ad.eq(0).find("input").val(data[7]);
            _ad.eq(1).find("input").val(data[8]);
            _ad.eq(2).find("input").val(data[9]);
            //_ad.eq(6).find("option").attr("selected",false);
           // console.log(_ad.eq(6));
        }
        else{
            alert('wc');
        }

        $("#btn1").data("targetId", pid);

    }
    $("body").delegate(".update", "click", function () {
    $("#btn4").bind("click",http_test);
                $td = $(this).parents("tr").find("td");
                // alert("===" + $(this).data("pid"));
                var api_pid = $td.eq(0).text();
                var list_api_param = [$td.eq(1).text(), " " +$td.eq(2).text(), " " +$td.eq(3).text(), " " + $td.eq(4).text() + " ", $td.eq(5).text() + " ", $td.eq(6).text() + " ", $td.eq(7).text() + " "];
                $('.theme-popover-mask').fadeIn(100);
                $('.theme-popover').slideDown(200, function () {
                    $.ajax({
                        url: "/httpUnionSearch",
                        type: "get",
                        data:{
                            project: $td.eq(1).text(),
                            case_api: $td.eq(2).text(),
                            pid: api_pid,
                            method: $td.eq(5).text()
                        }
                    }).done(function (result){
                        //alert(list_api_param);
                        //console.log(result);
                        var _temo = []
                        for (var i = 0; i < result['datas'].length; i++) {
                            _temo.push(result['datas'][i]);
                        }
                        changeTheme(_temo,api_pid);
                    });
                    //changeTheme([$td.eq(1).text(), " " +$td.eq(2).text(), " " +$td.eq(3).text(), " " + $td.eq(4).text() + " ", $td.eq(5).text() + " ", $td.eq(6).text() + " ", $td.eq(7).text() + " "], $td.eq(0).text())
                    initAPIparams($td.eq(5).text());
                });
        });//打开新增数据弹层
    $("#btn1").bind("click",save_http_data);
});


$("#btn5").click(function () {
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    var pid=$("#targetId").val();
    //alert(pid);
    var api_data=$("#get_params").val();
    var api_headers=$("#get_headers").val();
    var api_cookies=$("#get_cookies").val();
    var except_result=$("#except_result").val();
    if (pid==""||pid=="999999999"){
        //alert("/mock"+case_url);
        $.ajax({
            url: "/mock"+case_url,
            type: "post",
            data: {
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
            }
        }).done(function (result) {
                  alert(except_result);
               // $("#RS").html("");
                $("#RS").html(except_result);
                })
                }
    else{
        //alert(api_redirects)
        $.ajax({
            url: "/mock"+case_url,
            type: "post",
            data: {
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
                id: pid,
            }
        }).done(function (result) {
                alert(result);
               // $("#RS").html("");
                $("#RS").html(result);
                }
       );}
});





$(document).ready(changeAPIparams ());
function changeAPIparams(){
  $("#method").bind("change",function(){
    if($(this).val()=="GET"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(get_title);
        $("#apt_datas").append(get_data);
    }
    else if($(this).val()=="POST"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(post_title);
        $("#apt_datas").append(post_data);
    }
    else if ($(this).val()=="HEAD"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第HEAD行</td></tr>");
        $("#apt_datas").append("<tr><td>第HEAD行</td></tr>");
    }
    else if ($(this).val()=="PUT"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PUT行</td></tr>");
        $("#apt_datas").append("<tr><td>第PUT行</td></tr>");
     }
    else if ($(this).val()=="DELETE"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第DELETE行</td></tr>");
        $("#apt_datas").append("<tr><td>第DELETE行</td></tr>");
     }
    else if ($(this).val()=="OPTIONS"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第OPTIONS行</td></tr>");
        $("#apt_datas").append("<tr><td>第OPTIONS行</td></tr>");
     }
    else if ($(this).val()=="PATCH"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PATCH行</td></tr>");
        $("#apt_datas").append("<tr><td>第PATCH行</td></tr>");
      }
    else {
        $("#apt_title").html("");
        $("#apt_datas").html("");
    }
  });
}

function initAPIparams(method){
    if(method=="GET"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(get_title);
        $("#apt_datas").append(get_data);
    }
    else if(method=="POST"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(post_title);
        $("#apt_datas").append(post_data);

    }
    else if (method=="HEAD"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第HEAD行</td></tr>");
        $("#apt_datas").append("<tr><td>第HEAD行</td></tr>");
    }
    else if (method=="PUT"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PUT行</td></tr>");
        $("#apt_datas").append("<tr><td>第PUT行</td></tr>");
     }
    else if (method=="DELETE"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第DELETE行</td></tr>");
        $("#apt_datas").append("<tr><td>第DELETE行</td></tr>");
     }
    else if (method=="OPTIONS"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第OPTIONS行</td></tr>");
        $("#apt_datas").append("<tr><td>第OPTIONS行</td></tr>");
     }
    else if (method=="PATCH"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PATCH行</td></tr>");
        $("#apt_datas").append("<tr><td>第PATCH行</td></tr>");
      }
    else {
        $("#apt_title").html("");
        $("#apt_datas").html("");
    }
}

$("body").delegate(".delet","click", function(){
    $td = $(this).parents("tr").find("td");
    var api_pid = $td.eq(0).text();
    var status = $td.eq(8).text();
    //alert(status);
    if (status=="false"){
        case_status = 1;
    }
    else{
        case_status = 0;
    }
    //alert(status);
    $.ajax({
        url: "/httpDelete",
        type: "get",
        data:{
            pid: api_pid,
            status:case_status
    }}).done(function(result){
                    if (result.status == "200"){
                        alert(result.datas);
                        location.reload()}
                    else{
                        alert(result.datas);
                       }
                });
});

function addThreeTheam(theamClass){
var classProprety = theamClass;
 var cookies_html = "<div class=\"useBtnSaveParams add-"+classProprety+" cform\"><table id=\""+ classProprety +"Title\" border=\"5\" width=\"100%\"\n" +
                    "class=\"CSSearchTbl\" cellpadding=\"0\" cellspacing=\"0\">\n" +
                    "<tbody><tr><th style=\"width: 50%; height: 50%\">KEY</th>\n" +
                    "<th style=\"width: 50%; height: 50%\">VALUE</th></tr>\n" +
                    "</tbody><tbody id=\""+classProprety+"Value\"></tbody></table></div>\n" +
                    "<div class=\"btnDivBtn\">\n" +
                    "<button class=\"btn btn-default btnParamsSaveAdd "+classProprety+"Add\" onclick=\"addProprety('precondition')\">+</button>\n"+
                    "<button class=\"btn btn-default btnParamsSaveSub "+classProprety+"Sub\" onclick=\"subProprety('precondition')\">-</button>\n"+
                    "<button class=\"btn btn-default btnParamsSaveSave "+classProprety+"Save\" onclick=\"saveValues('"+classProprety+"Value','"+classProprety+"')\">Save</button></div>"
 $("."+classProprety).append(cookies_html);
 $("."+classProprety).css('display','block');
}
function addProprety(classProprety){
        $("#"+classProprety+"Value").append("<tr><td><input value=\"\" style=\"width: 100%; height: 100%\"></td><td><input value=\"\" style=\"width: 100%; height: 100%\"/></td></tr>");
}

function subProprety(classProprety){
        $("#"+classProprety+"Value tr").eq(-1).remove();
}

function saveValues(id,saveId){
  var datadict = new Object;
  var tb = document.getElementById(id);
  var rows = tb.rows;
  for (var i=0;i<rows.length;i++){
      datadict[rows[i].cells[0].childNodes[0].value]=rows[i].cells[1].childNodes[0].value;}
    //console.log(datadict);
  var date = JSON.stringify(datadict);
  console.log(date);
  $("#"+saveId).val(date);
  alert('数据保存成功');
  $(".theme-cookies").remove();
  //$(".theme-cookies").css('display','none');
};
$("#check1").change(function(){
 var scheduling=$("#check1").is(':checked');
 if (scheduling==true){
  $("#assert").attr('disabled',false);
 // $("#test_suite").attr('disabled',false);
 }
 else{
  $("#assert").attr('disabled',true);
 // $("#test_suite").attr('disabled',true);
 };
});
$("#check2").change(function(){
 var scheduling=$("#check2").is(':checked');
 if (scheduling==true){
  $("#account").attr('disabled',false);
 }else{
  $("#account").attr('disabled',true);
 };});
$("#check3").change(function(){
var upload_file=$("#check3").is(":checked");
if (upload_file==true){
    $("#btn4").unbind("click");  //取消btn4 运行测试点击事件
    $("#btn4").attr("id","btn6");　　//更改id=btn6(运行测试按钮)
    $("#btn6").bind("click",http_upload_test);  //btn6添加http_upload_test运行测试功能事件
    $("#apt_others").append(file_data);  //添加上传文件input 框

    $("#btn1").unbind("click");  //取消btn1 保存数据点击事件
    $("#btn1").attr("id","btn7");
    $("#btn7").bind("click",save_file_data);
}
else{
$("#btn6").unbind("click");　　//取消btn6绑定事件
$("#btn6").attr("id","btn4");　　//更改id=btn4(运行测试按钮)
$("#btn4").bind("click",http_test);  //btn4添加http_test运行测试功能事件
$("#apt_others").html("");  //清空上传文件input 框

$("#btn7").unbind("click");  //保存按钮解除保存文件事件
$("#btn7").attr("id","btn1");　　//id=btn1
$("#btn1").bind("click",save_http_data);  //btn1添加保存数据事件
};
});
function http_test () {
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    if (method=="GET"){
        var api_data=$("#get_params").val();
        var api_headers=$("#get_headers").val();
        var api_cookies=$("#get_cookies").val();
        var project_cn=$("#project_choice").val();
        var islogin=$("#check2").is(':checked');
        var account=$("#account").val();
        var upload_file=$("#check3").is(":checked");
        $.ajax({
            url: "/case_http_test",
            type: "post",
            data: {
                project_cn:project_cn,
                case_host: case_host,
                case_url: case_url,
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
                islogin: islogin,
                account: account,
                isUpload: upload_file,
                pid: $("#targetId").val(),
            }
        }).done(function (result) {
            if (result.code == "200")
            {var wc = result.datas;
                alert(wc);
               // $("#RS").html("");
                $("#RS").html(wc);
              }
            else{alert(result.code,result.datas);}
        });}
    else if (method=="POST") {
        var api_data = $("#post_params").val();
        var api_headers = $("#post_headers").val();
        var api_cookies = $("#post_cookies").val();
        var project_cn=$("#project_choice").val();
        var islogin=$("#check2").is(':checked');
        var account=$("#account").val();
        var upload_file=$("#check3").is(":checked");
        //alert(api_redirects)
        $.ajax({
            url: "/case_http_test",
            type: "post",
            data: {
                project_cn:project_cn,
                case_host: case_host,
                case_url: case_url,
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
                islogin: islogin,
                account: account,
                 isUpload: upload_file,
                pid: $("#targetId").val(),
            }
        }).done(function (result) {
            if (result.code == "200")
            {var wc = result.datas;
                alert(wc);
               // $("#RS").html("");
                $("#RS").html(wc);
            }
            else{alert(result.code,result.datas);}
        });}
};
function http_upload_test() {
               var fileObj = document.getElementById("FileUpload").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               var file_desc = $("#file_desc").val()
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象
               var data_flie = formFile;

               var case_host=$("#case_host").val();
                var case_url=$("#case_url").val();
                var method=$("#method").find("option:selected").val();
            if (method=="GET"){
                var api_data=$("#get_params").val();
                var api_headers=$("#get_headers").val();
                var api_cookies=$("#get_cookies").val();
                var project_cn=$("#project_choice").val();
                var islogin=$("#check2").is(':checked');
                var account=$("#account").val();
                   data_flie.append("project_cn",project_cn);
                    data_flie.append("case_host",case_host);
                    data_flie.append("case_url",case_url);
                    data_flie.append("method",method);
                    data_flie.append("params",api_data);
                    data_flie.append("headers",api_headers);
                    data_flie.append("cookies",api_cookies);
                    data_flie.append("islogin",islogin);
                    data_flie.append("account",account);
                    data_flie.append("file_desc",file_desc);
               $.ajax({
                        url: "/test_upload",
                        type: "post",
                        data: data_flie,
                        dataType: "json",
                        cache: false,//上传文件无需缓存
                        processData: false,//用于对data参数进行序列化处理 这里必须false
                        contentType: false, //必须
                    }).done(function (result) {
                    if (result.code == "200")
                    {var wc = result.datas;
                        alert(wc);
                       // $("#RS").html("");
                        $("#RS").html(wc);
                      }
                    else{alert(result.code,result.datas);}
                });}
            else if (method=="POST") {
                    var api_data = $("#post_params").val();
                    var api_headers = $("#post_headers").val();
                    var api_cookies = $("#post_cookies").val();
                    var project_cn=$("#project_choice").val();
                    var islogin=$("#check2").is(':checked');
                    var account=$("#account").val();
                    //alert(api_redirects)
                    data_flie.append("params",api_data);
                    data_flie.append("project_cn",project_cn);
                    data_flie.append("case_host",case_host);
                    data_flie.append("case_url",case_url);
                    data_flie.append("method",method);
                    data_flie.append("params",api_data);
                    data_flie.append("headers",api_headers);
                    data_flie.append("cookies",api_cookies);
                    data_flie.append("islogin",islogin);
                    data_flie.append("account",account);
                    data_flie.append("file_desc",file_desc);
                    $.ajax({
                        url: "/test_upload",
                        type: "post",
                        data: data_flie,
                        dataType: "json",
                        cache: false,//上传文件无需缓存
                        processData: false,//用于对data参数进行序列化处理 这里必须false
                        contentType: false, //必须
                    }).done(function (result) {
                        if (result.code == "200")
                        {var wc = result.datas;
                            alert(wc);
                           // $("#RS").html("");
                            $("#RS").html(wc);
                        }
                        else{alert(result.code,result.datas);}
                    });}
               };
function save_http_data () {
        var _case = [];
        var upload_file=$("#check3").is(":checked");
        $("#tbdata tr").each(function () {
            var tr = $(this);
            _case.push({
                project: $("#project_choice").find("option:selected").val(),
                case_api: $("#case_api").val(),
                case_desc: $("#case_desc").val(),
                case_host: $("#case_host").val(),
                case_url: $("#case_url").val(),
                method: $("#method").find("option:selected").val(),
                except_result: $("#except_result").val(),
                scheduling: $("#check1").is(':checked'),
                islogin: $("#check2").is(':checked'),
                assert: $("#assert").val(),
                account: $("#account").val(),
                //test_suite: $("#test_suite").val(),

            });
        });
        if ($("#targetId").val()!= "999999999" ) {
            //数据更新
            //alert(_case[0].method);
            if (_case[0].method=="GET"){
            $.ajax({
                url: "/httpUpdate",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#get_params").val(),
                    headers: $("#get_headers").val(),
                    cookies: $("#get_cookies").val(),
                    scheduling: $("#check1").is(':checked'),
                    islogin: $("#check2").is(':checked'),
                    assert: $("#assert").val(),
                    account: $("#account").val(),
                    upload_file:upload_file,
                //test_suite: $("#test_suite").val(),
                }}).done(function (result){
                    if (result.status == "200"){
                        alert(result.datas);
                        location.reload()}
                    else{
                        alert(result.datas);
                       }
                });
                }
            else if (_case[0].method=="POST"){
                $.ajax({
                url: "/httpUpdate",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#post_params").val(),
                    headers: $("#post_headers").val(),
                    cookies: $("#post_cookies").val(),
                    scheduling: $("#check1").is(':checked'),
                    islogin: $("#check2").is(':checked'),
                    assert: $("#assert").val(),
                    account: $("#account").val(),
                    upload_file:upload_file,
               // test_suite: $("#test_suite").val(),
                }
            }).done(function(result){
                    if (result.status == "200"){
                        alert(result.datas);
                        location.reload()}
                    else{
                        alert(result.datas);
                       }
                });
            }
        } else {
            //数据新增
            if (_case[0].method=="GET"){
            $.ajax({
                url: "/httpInsert",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#get_params").val(),
                    headers: $("#get_headers").val(),
                    cookies: $("#get_cookies").val(),
                    scheduling: $("#check1").is(':checked'),
                    islogin: $("#check2").is(':checked'),
                    upload_file:$("#check3").is(":checked"),
                assert: $("#assert").val(),
                account: $("#account").val(),
                upload_file:upload_file,
                //test_suite: $("#test_suite").val(),
                }
            }).done(function(result){
                    if (result.status == "200"){
                        alert(result.datas);
                        location.reload()}
                    else{
                        alert(result.datas);
                       }
                });;
                }
            else if (_case[0].method=="POST"){
                $.ajax({
                url: "/httpInsert",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#post_params").val(),
                    headers: $("#post_headers").val(),
                    cookies: $("#post_cookies").val(),
                    scheduling: $("#check1").is(':checked'),
                    islogin: $("#check2").is(':checked'),
                    upload_file:$("#check3").is(":checked"),
                assert: $("#assert").val(),
                account: $("#account").val(),
                    upload_file:upload_file,
               // test_suite: $("#test_suite").val(),
                }
            }).done(function(result){
                    if (result.status == "200"){
                        alert(result.datas);
                        location.reload()}
                    else{
                        alert(result.datas);
                       }
                });
            };}}
function save_file_data () {
    save_http_data();  //保存接口测试数据
    var project=$("#project_choice").find("option:selected").val();
    var case_api=$("#case_api").val();
    var case_desc=$("#case_desc").val();
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    var file_desc=$("#file_desc").val();
    var targetId=$("#targetId").val();
    var fileObj = document.getElementById("FileUpload").files[0]; // js 获取文件对象
    if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
        alert("请选择文件");
        return;}
    var formFile = new FormData();
    var file_desc = $("#file_desc").val()
    formFile.append("action", "UploadVMKImagePath");
    formFile.append("file", fileObj); //加入文件对象
    formFile.append("project",project);
    formFile.append("case_api",case_api);
    formFile.append("case_desc",case_desc);
    formFile.append("case_host",case_host);
    formFile.append("case_url",case_url);
    formFile.append("method",method);
    formFile.append("file_desc",file_desc);
    formFile.append("targetId",targetId);
               var data_flie = formFile;
               $.ajax({
                        url: "/save_upload_data",
                        type: "post",
                        data: data_flie,
                        dataType: "json",
                        cache: false,//上传文件无需缓存
                        processData: false,//用于对data参数进行序列化处理 这里必须false
                        contentType: false, //必须
                    }).done(function (result) {
                        if (result.code == "200")
                        {var wc = result.datas;
                            alert(wc);
                           // $("#RS").html("");
                            $("#RS").html(wc);}
                        else{alert(result.code,result.datas);}
                    });
};
function btn_clear(){
   var file = document.getElementById("FileUpload");
     // for IE, Opera, Safari, Chrome
     if (file.outerHTML) {
         file.outerHTML = file.outerHTML;
     } else { // FF(包括3.5)
         file.value = "";
     }
   };
