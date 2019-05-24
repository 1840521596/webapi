
$("#btn2").click(function () {
    $.ajax({
        url: "/projectSearch",
        type: "get",
        data: {
            project: $("#project").find("option:selected").val()
        }
    }).done(function (result) {
        if (result.status == "200")
        {
            var _temo = [];
            // alert(result['datas']);
            for (var i = 0; i < result['datas'].length; i++) {
                _temo.push(result['datas'][i]);
            }
            var tableHTML = "";
            // alert(_temo);
            // alert(_temo);
            for (var i = 0; i < _temo.length; i++) {
                var j = i + 1;
                tableHTML = tableHTML + '<tr><td style="display:none">' + j + '</td><td >' + _temo[i][0] + '</td><td>' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td></tr>';
            }//case_name+description+case_url+method+parameter+assert
            $("#casetb").html(tableHTML);
            // alert(tableHTML);
        }
        else{
            alert(result.error);
        }
    })
});

$(document).ready(function () {
//    $.ajax({
//        url: "http://uwsgi.sys.bandubanxie.com/projectSearch",
//        type: "get",
//        data: {
//            project: $("#project").find("option:selected").val()
//        }
//    }).done(function (result) {
//        if (result.status == "200") {
//            var _temo = [];
//            // alert(result['datas']);
//            for (var i = 0; i < result['datas'].length; i++) {
//                _temo.push(result['datas'][i]);
//            }
//            var tableHTML = "";
//            // alert(_temo);
//            // alert(_temo);
//            for (var i = 0; i < _temo.length; i++) {
//                var j = i + 1;
//                tableHTML = tableHTML + '<tr><td style="display:none">' + j + '</td><td >' + _temo[i][0] + '</td><td>' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td></tr>';
//            }//case_name+description+case_url+method+parameter+assert
//            $("#casetb").html(tableHTML);
//            // alert(tableHTML);
//        }
//        else{
//            alert(result.error);
//        }
//    });

    $('.theme-login').click(function () {
        $('.theme-popover-mask').fadeIn(100);
        $("#project_name").val("");
        $("#project_domain").val("");
        $("#RC").val("");
        $('.theme-popover').slideDown(200);
    });
    $('.theme-poptit .close').click(function () {
        $('.theme-popover-mask').fadeOut(100);
        $('.theme-popover').slideUp(200, function () {
        });
    });

    $("#btn1").click(function () {
        var _case = []
        $("#tbdata tr").each(function () {
            var tr = $(this)
            var svn_url_str;
            _case.push({
                project: $("#project_name").val(),
                domain: $("#project_domain").val(),
                description:$("#RC").val()
            });
        });
        //alert(_case[0]);
        if ($(this).data("targetId") && $(this).data("targetId") !== 0) {
            //数据更新
            $.ajax({
                url: "/projectUpdate",
                type: "get",
                data: {
                    project: $("#project_name").val(),
                    domain: $("#project_domain").val(),
                    description:$("#RC").val(),
                },
                success: function () {
                    alert("保存成功")
                    $.cookie('feature', _case[0].feature);
                    $.cookie('scene', _case[0].scene);
                    $("#feature").text($.cookie('feature'))
                    $("#scene").text($.cookie('scene'))
                    location.reload()
                }
            })
        } else {
            //数据新增
            $.ajax({
                url: "/projectInsert",
                type: "get",
                data: {
                    project: $("#project_name").val(),
                    project_en: $("#project_en").val(),
                    domain: $("#project_domain").val(),
                    description:$("#RC").val()
                }}).done(function (result) {
                if (result.status == "200")
                    {
                    alert("保存成功");
                    $.ajax({
                        url: "/projectSearch",
                        type: "get",
                        data: {
                            project: $("#project").find("option:selected").val()
                        }
                    }).done(function (result) {
                        var _temo = [];
                        // alert(result['datas']);
                        for (var i = 0; i < result['datas'].length; i++) {
                            _temo.push(result['datas'][i]);
                        }
                        var tableHTML = "";
                        // alert(_temo);
                        for (var i = 0; i < _temo.length; i++) {
                            var j = i + 1;
                            tableHTML = tableHTML + '<tr><td style="display:none">' + j + '</td><td >' + _temo[i][0] + '</td><td>' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td></tr>';
                        }//case_name+description+case_url+method+parameter+assert
                        $("#casetb").html(tableHTML);
                        $('.theme-popover-mask').fadeOut(100);
                        $('.theme-popover').slideUp(200);})
                    }
                    else{
                        alert("保存失败");
                        alert(result.result)
                        }
                    })
            }
    });
});
