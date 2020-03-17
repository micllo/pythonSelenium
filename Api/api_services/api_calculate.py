# -*- coding:utf-8 -*-
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


def sync_run_case(pro_name, browser_name, thread_num):
    """
    同时执行不同的用例
    :param pro_name
    :param browser_name: Chrome、Firefox
    :param thread_num: 线程数
    :return:
    """
    pool = ThreadPoolExecutor(1)
    from Common.sync_run_case import suite_sync_run_case
    pool.submit(suite_sync_run_case, pro_name=pro_name, browser_name=browser_name,
                thread_num=thread_num, remote=cfg.REMOTE)


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
    将某项目的所有测试用例同步入mongo库中，默认状态为'下线'
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
                test_case_dict["case_status"] = False
                test_case_dict["run_status"] = False
                test_case_dict["last_run_time"] = ISODate
                test_case_dict["create_time"] = ISODate
                insert_list.append(test_case_dict)
        # 将'测试用例'列表更新入对应项目的数据库中
        with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
            try:
                pro_db.drop()
                pro_db.insert_many(insert_list)
            except Exception as e:
                mongo_exception_send_DD(e=e, msg="更新'" + pro_name + "'项目测试用例数据")
                return "mongo error"
        return insert_list
    else:
        return "no such pro"


def update_case_status(pro_name, test_method_name):
    """
    更新某个'测试用例'的'状态'(上下线)
    :param pro_name:
    :param test_method_name:
    :return:
    """
    with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
        try:
            query_dict = {"test_method_name": test_method_name}
            result = pro_db.find_one(query_dict, {"_id": 0})
            old_case_status = result.get("case_status")
            new_case_status = bool(1 - old_case_status)  # 布尔值取反
            update_dict = {"$set": {"case_status": new_case_status}}
            pro_db.update_one(query_dict, update_dict)
            return new_case_status
        except Exception as e:
            mongo_exception_send_DD(e=e, msg="更新'" + pro_name + "'项目测试用例状态(单个)")
            return "mongo error"


def update_case_status_all(pro_name, case_status=False):
    """
    更新'某项目'的所有测试用例'状态'(上下线)
    :param pro_name:
    :param case_status:
    :return: 返回 test_method_name_list 列表
    """
    with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
        try:
            update_dict = {"$set": {"case_status": case_status}}
            pro_db.update({}, update_dict, multi=True)
            results = pro_db.find({}, {"_id": 0})
            return [res.get("test_method_name") for res in results]
        except Exception as e:
            mongo_exception_send_DD(e=e, msg="更新'" + pro_name + "'项目测试用例状态(批量)")
            return "mongo error"


def get_test_case(pro_name):
    """
    根据'项目名称'获取'测试用例'列表（上线的排在前面）
    :param pro_name:
    :return:
    """
    test_case_list = []
    on_line_list = []
    off_line_list = []
    with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
        try:
            results = pro_db.find({}, {"_id": 0})
            for res in results:
                test_case_dict = dict()
                test_case_dict["case_status"] = res.get("case_status")
                test_case_dict["test_case_name"] = res.get("test_case_name")
                test_case_dict["test_class_name"] = res.get("test_class_name")
                test_case_dict["test_method_name"] = res.get("test_method_name")
                test_case_dict["run_status"] = res.get("run_status")
                test_case_dict["last_run_time"] = res.get("last_run_time")
                test_case_dict["create_time"] = res.get("create_time")
                if res.get("case_status"):
                    on_line_list.append(test_case_dict)
                else:
                    off_line_list.append(test_case_dict)
            test_case_list = on_line_list + off_line_list
        except Exception as e:
            mongo_exception_send_DD(e=e, msg="获取'" + pro_name + "'项目测试用例列表")
            return "mongo error"
        finally:
            return test_case_list


def stop_case_run_status(pro_name):
    """
    强行修改用例运行状态 -> 停止
    :param pro_name:
    :return:
    """
    with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
        try:
            update_dict = {"$set": {"run_status": False}}
            pro_db.update({}, update_dict, multi=True)
            return True
        except Exception as e:
            mongo_exception_send_DD(e=e, msg="更新'" + pro_name + "'项目测试用例状态(批量)")
            return "mongo error"



if __name__ == "__main__":
    pass
    # clear_screen_shot(4)
    # case_import_mongo("pro_demo_1")
    # update_case_status("pro_demo_1", "test_02")
    # update_case_status_all(pro_name="pro_demo_1", status=False)
