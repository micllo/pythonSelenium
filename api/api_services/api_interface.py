# -*- coding: utf-8 -*-
"""
api 服务接口
"""
from api import flask_app
import json
from Config.error_mapping import *
from api.api_services.api_template import interface_template
from api.api_services.api_calculate import sync_run_case_exec


@flask_app.route("/UI/sync_run_case/<browser_name>", methods=["GET"])
def sync_run_case(browser_name):
    """
    同时执行不同的用例 (开启线程执行，直接返回接口结果)
    :param browser_name: Chrome、Firefox
    :return:
    """
    result_dict = {"browser_name": browser_name}
    if browser_name in ["Chrome", "Firefox"]:
        sync_run_case_exec(browser_name)
        error_msg = CASE_RUNING
    else:
        error_msg = BROWSER_NAME_ERROR
    re_dict = interface_template(error_msg, result_dict)
    return json.dumps(re_dict, ensure_ascii=False)

