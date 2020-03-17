/**
 * 修改案件状态（单个）
 */
function update_case_status(pro_name, test_method_name, nginx_api_proxy) {
    // 调用ajax请求(同步)
    var request_url = "/" + nginx_api_proxy + "/WEB/set_case_status/" + pro_name + "/" + test_method_name
    var response_info = request_interface_url_v2(url=request_url, method="GET", async=false);
    if(response_info != "请求失败"){
        if(response_info.data.new_case_status == true){
            $("#off_line_" + test_method_name).html("上 线");
            $("#off_line_" + test_method_name).removeClass("btn btn-danger btn-sm").addClass("btn btn-success btn-sm");
            $("#off_line_" + test_method_name + "_tr").removeClass("passClass danger").addClass("passClass success");
        }else{
            $("#on_line_" + test_method_name).html("下 线");
            $("#on_line_" + test_method_name).removeClass("btn btn-success btn-sm").addClass("btn btn-danger btn-sm");
            $("#on_line_" + test_method_name + "_tr").removeClass("passClass success").addClass("passClass danger");
        }
    }
}


/**
 * 修改案件状态（所有）
 */
function update_case_status_all(pro_name, case_status, nginx_api_proxy) {
    // 调用ajax请求(同步)
    var request_url = "/" + nginx_api_proxy + "/WEB/set_case_status_all/" + pro_name + "/" + case_status
    var response_info = request_interface_url_v2(url=request_url, method="GET", async=false);
    if(response_info != "请求失败"){
        $.each(response_info.data.test_method_name_list,function (i, test_method_name) {
            if(case_status == "true"){
                $("#off_line_" + test_method_name).html("上 线");
                $("#off_line_" + test_method_name).removeClass("btn btn-danger btn-sm").addClass("btn btn-success btn-sm");
                $("#off_line_" + test_method_name + "_tr").removeClass("passClass danger").addClass("passClass success");
            }else{
                $("#on_line_" + test_method_name).html("下 线");
                $("#on_line_" + test_method_name).removeClass("btn btn-success btn-sm").addClass("btn btn-danger btn-sm");
                $("#on_line_" + test_method_name + "_tr").removeClass("passClass success").addClass("passClass danger");
            }
        })
    }
}


/**
 * 批量执行
 */
function run_case(pro_name, nginx_api_proxy) {
    swal({
        title: "确 定 执 行 用 例 吗 ?",
        text: "",
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消"
    }).then(function(isConfirm){
        if (isConfirm) {
            // 调用ajax请求(同步)
            var request_url = "/" + nginx_api_proxy + "/WEB/sync_run_case/" + pro_name
            var data_dict = {"browser_name": "Chrome", "thread_num": 2}
            var response_info = request_interface_url_v2(url=request_url, method="POST", data=data_dict, async=false);
            if(response_info == "请求失败"){
                swal({text: response_info, type: "error", confirmButtonText: "知道了"});
            }else{
               if(response_info.status == "success"){
                   swal({text: response_info.msg, type: "success", confirmButtonText: "知道了"});
                   setTimeout(function(){location.reload();}, 3000);
                }else{
                   swal({text: response_info.msg, type: "error", confirmButtonText: "知道了"});
                }
            }
        }
    }).catch((e) => {
        console.log(e)
        console.log("cancel");
    });
}


/**
 * 同步用例列表
 */
function sync_case_list(pro_name, nginx_api_proxy) {
    swal({
        title: "确 定 要 同 步 用 例 吗 ?",
        text: "",
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消"
    }).then(function(isConfirm){
        if (isConfirm) {
            // 调用ajax请求(同步)
            var request_url = "/" + nginx_api_proxy + "/WEB/sync_case_list/" + pro_name
            var response_info = request_interface_url_v2(url=request_url, method="GET", async=false);
            if(response_info == "请求失败"){
                swal({text: response_info, type: "error", confirmButtonText: "知道了"});
            }else{
               if(response_info.status == "success"){
                   swal({text: response_info.msg, type: "success", confirmButtonText: "知道了"});
                   setTimeout(function(){location.reload();}, 3000);
                }else{
                   swal({text: response_info.msg, type: "error", confirmButtonText: "知道了"});
                }
            }
        }
    }).catch((e) => {
        console.log(e)
        console.log("cancel");
    });
}


/**
 * 强行修改用例运行状态 -> 停止
 */
function stop_run_status(pro_name, nginx_api_proxy) {
    swal({
        title: "确 定 要 修 改 运 行 状 态 吗 ?",
        text: "",
        type: "warning",
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消"
    }).then(function(isConfirm){
        if (isConfirm) {
            // 调用ajax请求(同步)
            var request_url = "/" + nginx_api_proxy + "/WEB/stop_run_status/" + pro_name
            var response_info = request_interface_url_v2(url=request_url, method="GET", async=false);
            if(response_info == "请求失败"){
                swal({text: response_info, type: "error", confirmButtonText: "知道了"});
            }else{
               if(response_info.status == "success"){
                   swal({text: response_info.msg, type: "success", confirmButtonText: "知道了"});
                   setTimeout(function(){location.reload();}, 3000);
                }else{
                   swal({text: response_info.msg, type: "error", confirmButtonText: "知道了"});
                }
            }
        }
    }).catch((e) => {
        console.log(e)
        console.log("cancel");
    });
}



// // 将按钮禁灰不可点击
// var btn = document.getElementById("stop_run_status");
// btn.setAttribute('disabled', 'true');
//
// // 改变当前结果状态
// $("#stop_run_status_result").html(" 处 理 中 。。。");
// $("#stop_run_status_result").removeClass().addClass("label label-info");
//
// $("#stop_run_status_result").html(response_info.msg);
// $("#stop_run_status_result").removeClass().addClass("label label-success");
// $("#stop_run_status_result").removeClass().addClass("label label-warning");
// $("#stop_run_status_result").removeClass().addClass("label label-danger");
//
// // 将按钮还原可点击
// var btn = document.getElementById("stop_run_status");
// btn.removeAttribute('disabled');