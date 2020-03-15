/**
 * 修改案件状态（单个）
 * @param guava_url
 */
function update_case_status(pro_name, test_method_name, nginx_api_proxy) {
    // 调用ajax同步请求
    var request_url = "/" + nginx_api_proxy + "/UI/set_case_status/" + pro_name + "/" + test_method_name
    var response_info = request_interface_url_v2(url=request_url, method="GET", async=false);
    if(response_info != ""){
        if(response_info.data.new_status == true){
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
 * @param guava_url
 */
function update_case_status_all(pro_name, status, nginx_api_proxy) {
    // 调用ajax同步请求
    var request_url = "/" + nginx_api_proxy + "/UI/set_case_status_all/" + pro_name + "/" + status
    var response_info = request_interface_url_v2(url=request_url, method="GET", async=false);
    if(response_info != ""){
        $.each(response_info.data.test_method_name_list,function (i, test_method_name) {
            if(status == "true"){
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