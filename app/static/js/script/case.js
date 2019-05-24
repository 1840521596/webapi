var get_title="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" width=\"20%\">Params(参数）</th>\n" +
    "       <th colspan=\"3\" width=\"20%\">Headers(标头)</th>\n" +
    "       <th colspan=\"2\" width=\"20%\">Cookies(缓存)</th>\n" +
    "      </tr>";
var get_data="<tr height=\"36px\">\n" +
    "<td colspan=\"3\"><input style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_params\" placeholder=\"测试数据\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='测试数据'\"></td>\n" +
    "<td colspan=\"3\"><input style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_headers\" placeholder=\"Headers\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Headers'\"></td>\n" +
    "<td colspan=\"2\"><input style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_cookies\" placeholder=\"Cookies\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Cookies'\"></td>\n" +
    "</tr>"


var post_title="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" width=\"20%\">Data(参数）</th>\n" +
    "       <th colspan=\"3\" width=\"20%\">Headers(标头)</th>\n" +
    "       <th colspan=\"2\" width=\"15%\">Cookies(缓存)</th>\n" +
    "      </tr>";

var post_data="<tr height=\"36px\">\n" +
    "<td colspan=\"3\"><input style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_params\" placeholder=\"测试数据\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='测试数据'\"></td>\n" +
    "<td colspan=\"3\"><input style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_headers\" placeholder=\"Headers\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Headers'\"></td>\n" +
    "<td colspan=\"2\"><input style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_cookies\" placeholder=\"Cookies\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Cookies'\"/></td>\n" +
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
                tableHTML = tableHTML + '<tr><td id="pid" style="display:none">' + _temo[i][0] + '</td><td >' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td><td>' + _temo[i][4] + '</td><td>' + _temo[i][5] + '</td><td style="display:none">' + _temo[i][6] + '</td><td style="display:none">' + _temo[i][7] + '</td><td style="display:none">'+ _temo[i][8] + '</td><td style="text-align: center;"><a data-pid="' + _temo[i][0] + '"class="btn btn-primary btn-large theme-login update">修改</a>&nbsp&nbsp&nbsp&nbsp<a data-pid="0"class="btn btn-primary btn-large theme-login delet">激活</a></td></tr>'}
                else{
                    tableHTML = tableHTML + '<tr><td id="pid" style="display:none">' + _temo[i][0] + '</td><td >' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td><td>' + _temo[i][4] + '</td><td>' + _temo[i][5] + '</td><td style="display:none">' + _temo[i][6] + '</td><td style="display:none">' + _temo[i][7] + '</td><td style="display:none">'+ _temo[i][8] + '</td><td style="text-align: center;"><a data-pid="' + _temo[i][0] + '"class="btn btn-primary btn-large theme-login update">修改</a>&nbsp&nbsp&nbsp&nbsp<a data-pid="1"class="btn btn-primary btn-large theme-login delet">冻结</a></td></tr>'
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
    })
    $('.theme-poptit .close').click(function () {
        $('.theme-popover-mask').fadeOut(100);
        $('.theme-popover').slideUp(200, function () {
            var _td = $("#tbdata").find("td");
        });
        location.reload();
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
    $("#btn1").click(function () {
        var _case = [];
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
            });
        });
        //alert($("#targetId").val());
        if ($("#targetId").val() && $("#targetId").val() !== 0) {
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
                    cookies: $("#get_cookies").val()
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
                    cookies: $("#post_cookies").val()
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
                    pid: $(this).data("targetId"),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#get_params").val(),
                    headers: $("#get_headers").val(),
                    cookies: $("#get_cookies").val()}
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
                    pid: $(this).data("targetId"),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#post_params").val(),
                    headers: $("#post_headers").val(),
                    cookies: $("#post_cookies").val()
                }
            }).done(function(result){
                    if (result.status == "200"){
                        alert(result.datas);
                        location.reload()}
                    else{
                        alert(result.datas);
                       }
                });
            };}});
});
$("#btn4").click(function () {
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    if (method=="GET"){
        var api_data=$("#get_params").val();
        var api_headers=$("#get_headers").val();
        var api_cookies=$("#get_cookies").val();
        $.ajax({
            url: "/case_http_test",
            type: "post",
            data: {
            case_host: case_host,
                case_url: case_url,
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
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
        //alert(api_redirects)
        $.ajax({
            url: "/case_http_test",
            type: "post",
            data: {
                case_host: case_host,
                case_url: case_url,
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies
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
}