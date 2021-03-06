# -*- coding: utf-8 -*-

"""
接口的输出模板处理
"""
from Config.error_mapping import *
from Common.date_helper import current_date


def interface_template(error_msg, result_dict):
    """
    接口返回的模板样式

    :param error_msg: 返回错误信息
    :param result_dict: 返回结果
    :return:
    """
    # 初始化模板模板
    res_dict = {"error_code": "", "error_msg": error_msg, "update_time": current_date(), "result": result_dict,
                "status": ""}
    # 查询错误码
    error_code = get_error_code(error_msg)
    res_dict["error_code"] = error_code
    if error_code == 31200:
        res_dict["status"] = "success"
    else:
        res_dict["status"] = "fail"

    return res_dict
