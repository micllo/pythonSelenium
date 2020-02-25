# -*- coding: utf-8 -*-
"""
api 服务接口
"""
from Api import flask_app
import json
from Config.error_mapping import *
from Api.api_services.api_template import interface_template
from Api.api_services.api_calculate import sync_run_case_exec
from Common.function import is_null
from flask import request


@flask_app.route("/UI/sync_run_case", methods=["POST"])
def sync_run_case():
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
        error_msg = PARAMS_NOT_NONE
    elif browser_name not in ["Chrome", "Firefox"]:
        error_msg = BROWSER_NAME_ERROR
    elif thread_num not in range(1, 6):  # 线程数量范围要控制在1~5之间
        error_msg = THREAD_NUM_ERROR
    else:
        sync_run_case_exec(browser_name, thread_num)
        error_msg = CASE_RUNING
    re_dict = interface_template(error_msg, result_dict)
    return json.dumps(re_dict, ensure_ascii=False)

