# -*- coding: utf-8 -*-
from Api import *
import json
from Config.error_mapping import *
from Api.api_services.api_template import interface_template
from Api.api_services.api_calculate import *
from Common.com_func import is_null, log
from Tools.mongodb import MongoGridFS
from Config import config as cfg
from Config.pro_config import pro_exist
from Config import global_var as gv

"""
api 服务接口
"""


@flask_app.route("/WEB/sync_run_case/<pro_name>", methods=["POST"])
def run_case(pro_name):
    """
    同时执行不同的用例 (开启线程执行，直接返回接口结果)
    :param pro_name:
    :return:

    browser_name: Chrome、Firefox
    thread_num: 线程数
    """
    params = request.json
    browser_name = params.get("browser_name") if params.get("browser_name") else None
    thread_num = params.get("thread_num") if params.get("thread_num") else None
    if not pro_exist(pro_name):
        msg = PRO_NOT_EXIST
    elif is_null(browser_name) or is_null(thread_num):
        msg = PARAMS_NOT_NONE
    elif browser_name not in ["Chrome", "Firefox"]:
        msg = BROWSER_NAME_ERROR
    elif thread_num not in range(1, 6):  # 线程数量范围要控制在1~5之间
        msg = THREAD_NUM_ERROR
    else:
        if gv.RUN_FLAG:
            msg = EXIST_RUNNING_CASE
        else:
            sync_run_case(pro_name, browser_name, thread_num)
            msg = CASE_RUNING
    result_dict = {"pro_name": pro_name, "browser_name": browser_name, "thread_num": thread_num}
    re_dict = interface_template(msg, result_dict)
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/get_img/5e61152ff0dd77751382563f
@flask_app.route("/WEB/get_img/<file_id>", methods=["GET"])
def get_screenshot_img(file_id):
    """
    获取截屏图片
    :param file_id:
    :return: 1.获取成功、2.找不到该文件、3.mongo连接不上
    """
    if is_null(file_id):
        msg = PARAMS_NOT_NONE
        img_base64 = ""
    else:
        mgf = MongoGridFS()
        img_base64 = mgf.get_base64_by_id(file_id)
        if is_null(img_base64):
            msg = MONGO_CONNECT_FAIL
        elif img_base64 == "no such file":
            msg = NO_SUCH_FILE
        else:
            msg = REQUEST_SUCCESS
            # response = make_response(img_base64)
            # response.headers.set('Content-Type', 'image/png')
            # return response
    re_dict = interface_template(msg, {"file_id": file_id, "img_base64": img_base64})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/update_project_case/pro_demo_1
@flask_app.route("/WEB/update_project_case/<pro_name>", methods=["GET"])
def update_project_case(pro_name):
    """
    更新指定项目的"测试用例"集合，默认状态为'下线'
    :param pro_name:
    :return:
    """
    if is_null(pro_name):
        msg = PARAMS_NOT_NONE
    else:
        insert_result = case_import_mongo(pro_name)
        if insert_result == "mongo error":
            msg = MONGO_CONNECT_FAIL
        elif insert_result == "no such pro":
            msg = NO_SUCH_PRO
        else:
            msg = REQUEST_SUCCESS
    re_dict = interface_template(msg, {"pro_name": pro_name})
    log.info(re_dict)
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/set_case_status/pro_demo_1/test_02
@flask_app.route("/WEB/set_case_status/<pro_name>/<test_method_name>", methods=["GET"])
def set_case_status(pro_name, test_method_name):
    """
    设置某个'测试用例'的'状态'(上下线)
    :param pro_name:
    :param test_method_name:
    :return:
    """
    new_status = None
    if is_null(pro_name) or is_null(test_method_name):
        msg = PARAMS_NOT_NONE
    else:
        new_status = update_case_status(pro_name, test_method_name)
        msg = new_status == "mongo error" and MONGO_CONNECT_FAIL or REQUEST_SUCCESS
    re_dict = interface_template(msg, {"pro_name": pro_name, "test_method_name": test_method_name,
                                       "new_status": new_status})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/set_case_status_all/pro_demo_1/false
@flask_app.route("/WEB/set_case_status_all/<pro_name>/<status>", methods=["GET"])
def set_case_status_all(pro_name, status):
    """
    设置整个项目的'测试用例'的'状态'(上下线)
    :param pro_name:
    :param status:
    :return:
    """
    test_method_name_list = []
    if is_null(pro_name) or is_null(status):
        msg = PARAMS_NOT_NONE
    else:
        if status in [True, False, "false", "FALSE", "TRUE", "true"]:
            status = status in [True, "TRUE", "true"] and True or False
            res = update_case_status_all(pro_name, status)
            if res == "mongo error":
                msg = MONGO_CONNECT_FAIL
            else:
                msg = REQUEST_SUCCESS
                test_method_name_list = res
        else:
            msg = REQUEST_ARGS_WRONG
    re_dict = interface_template(msg, {"pro_name": pro_name, "status": status,
                                       "test_method_name_list": test_method_name_list})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/get_test_case_list/pro_demo_1
@flask_app.route("/WEB/get_test_case_list/<pro_name>", methods=["GET"])
def get_test_case_list(pro_name):
    result_dict = dict()
    result_dict["nginx_api_proxy"] = cfg.NGINX_API_PROXY
    result_dict["pro_name"] = pro_name
    result_dict["test_case_list"] = get_test_case(pro_name)
    result_dict["current_report_url"] = cfg.CURRENT_REPORT_URL
    result_dict["history_report_path"] = cfg.HISTORY_REPORT_PATH
    result_dict["run_flag"] = gv.RUN_FLAG
    return render_template('case_status.html', tasks=result_dict)


# http://127.0.0.1:8070/api_local/WEB/index
@flask_app.route("/WEB/index", methods=["GET"])
def show_index():
    result_dict = dict()
    result_dict["nginx_api_proxy"] = cfg.NGINX_API_PROXY
    result_dict["api_addr"] = cfg.API_ADDR
    return render_template('index.html', tasks=result_dict)









