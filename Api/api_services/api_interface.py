# -*- coding: utf-8 -*-
"""
api 服务接口
"""
from Api import flask_app
import json
from Config.error_mapping import *
from Api.api_services.api_template import interface_template
from Api.api_services.api_calculate import sync_run_pro_demo_1, case_import_mongo
from Common.com_func import is_null, log
from flask import request
from Tools.mongodb import MongoGridFS


@flask_app.route("/UI/sync_run_case/pro_demo_1", methods=["POST"])
def test_pro_demo_1():
    """
    同时执行不同的用例 (开启线程执行，直接返回接口结果)
    browser_name: Chrome、Firefox
    thread_num: 线程数
    :return:
    """
    params = request.json
    browser_name = params.get("browser_name") if params.get("browser_name") else None
    thread_num = params.get("thread_num") if params.get("thread_num") else None
    print(browser_name)
    print(thread_num)
    print(type(thread_num))

    result_dict = {"browser_name": browser_name, "thread_num": thread_num}
    if is_null(browser_name) or is_null(thread_num):
        msg = PARAMS_NOT_NONE
    elif browser_name not in ["Chrome", "Firefox"]:
        msg = BROWSER_NAME_ERROR
    elif thread_num not in range(1, 6):  # 线程数量范围要控制在1~5之间
        msg = THREAD_NUM_ERROR
    else:
        sync_run_pro_demo_1(browser_name, thread_num)
        msg = CASE_RUNING
    re_dict = interface_template(msg, result_dict)
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8081/UI/get_img/5e61152ff0dd77751382563f
@flask_app.route("/UI/get_img/<file_id>", methods=["GET"])
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


@flask_app.route("/UI/update_project_case/<pro_name>", methods=["GET"])
def update_project_case(pro_name):
    """
    更新指定项目的"测试用例"名称，默认状态为'下线'
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










