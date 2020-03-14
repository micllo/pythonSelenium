# -*- coding:utf-8 -*-
from Common.sync_run_case import suite_sync_run_case
from concurrent.futures import ThreadPoolExecutor
from Config import config as cfg
from Common.com_func import log, is_null
from Common.test_func import mongo_exception_send_DD
import sys, os, time
from Tools.mongodb import MongoGridFS
from Tools.date_helper import get_date_by_days
from Tools.mongodb import MongodbUtils
from dateutil import parser
import unittest
from Config.pro_config import get_test_class_list_by_pro_name

# sys.path.append("./")


"""
api 服务底层的业务逻辑
"""


def sync_run_pro_demo_1(browser_name, thread_num):
    """
    同时执行不同的用例
    :param browser_name: Chrome、Firefox
    :param thread_num: 线程数
    :return:
    """
    pool = ThreadPoolExecutor(1)
    pool.submit(suite_sync_run_case, pro_name="pro_demo_1", browser_name=browser_name, thread_num=thread_num, remote=True)


def clear_reports_logs(time):
    """
    删除指定时间之前 生成的报告和日志
      -mmin +1 -> 表示1分钟前的
      -mtime +1 -> 表示1天前的
    :param time:
    :return:
    """
    rm_log_cmd = "find '" + cfg.LOGS_PATH + "' -name '*.log' -mmin +" + str(time) + " -type f -exec rm -rf {} \\;"
    rm_report_cmd = "find '" + cfg.REPORTS_PATH + "history' -name '*.html' -mmin +" + str(time) + \
                    " -type f -exec rm -rf {} \\;"
    print(rm_log_cmd)
    print(rm_report_cmd)
    os.system(rm_log_cmd)
    os.system(rm_report_cmd)


def clear_screen_shot(days):
    """
    删除指定日期之前的所有的截图
    :param days:
    :return:
    """
    date_str = get_date_by_days(days=days, time_type="%Y-%m-%dT%H:%M:%S")
    mgf = MongoGridFS()
    del_num = mgf.del_file_by_date(date_str)
    if is_null(del_num):
        log.error("\n清理'" + date_str + "'之前的截图时出错了！\n")
    else:
        log.info("\n已清理'" + date_str + "'之前的截图：" + str(del_num) + " 个\n")


def case_import_mongo(pro_name):
    """
    将所有指定'项目'的'测试用例名称'导入mongo库中，默认状态为'下线'
    :param pro_name:
    :return:
    [{"pro_name":"", "test_class_name":"", "test_method_name": "" ,"test_case_name": "" , "status": "", "create_time": ""}, {}]
    """
    test_class_list = get_test_class_list_by_pro_name(pro_name)
    if test_class_list:
        insert_list = []
        now_str = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
        ISODate = parser.parse(now_str)
        test_loader = unittest.TestLoader()
        for test_class in test_class_list:
            test_methods_name = test_loader.getTestCaseNames(test_class)
            for test_method_name in test_methods_name:
                # 生成'测试方法'的实例对象，并反射获取'测试方法'
                test_instance = test_class(test_method=test_method_name)
                testMethod = getattr(test_instance, test_method_name)
                # 获取'测试方法'中的备注，作为'测试用例名称'
                test_case_name = testMethod.__doc__.split("\n")[0].strip()
                test_case_dict = {}
                test_case_dict["pro_name"] = pro_name
                test_case_dict["test_class_name"] = test_class.__name__
                test_case_dict["test_method_name"] = test_method_name
                test_case_dict["test_case_name"] = test_case_name
                test_case_dict["status"] = False
                test_case_dict["create_time"] = ISODate
                insert_list.append(test_case_dict)
        # 将'测试用例'列表更新入对应项目的数据库中
        with MongodbUtils(ip=cfg.MONGODB_ADDR, database="web_auto_test", collection=pro_name) as monitor_db:
            try:
                monitor_db.drop()
                monitor_db.insert_many(insert_list)
            except Exception as e:
                mongo_exception_send_DD(e=e, msg="更新'" + pro_name + "'项目测试用例数据")
                return "mongo error"
        return insert_list
    else:
        return "no such pro"


if __name__ == "__main__":
    pass
    # clear_screen_shot(4)
    case_import_mongo("pro_demo_1")
