# -*- coding:utf-8 -*-
from Common.sync_run_case import suite_sync_run_case
from concurrent.futures import ThreadPoolExecutor
from TestCases.demo_test import DemoTest
from TestCases.train_test import TrainTest
from Config import config as cfg
from Common.com_func import log, is_null
import sys, os
from Tools.mongodb import MongoGridFS
from Tools.date_helper import get_date_by_days

sys.path.append("./")

"""
api 服务底层的业务逻辑
"""


def sync_run_case_exec(browser_name, thread_num):
    """
    同时执行不同的用例
    :param browser_name: Chrome、Firefox
    :param thread_num: 线程数
    :return:
    """
    pool = ThreadPoolExecutor(1)
    pool.submit(suite_sync_run_case, browser_name=browser_name, test_class_list=[TrainTest, DemoTest],
                thread_num=thread_num, remote=True)


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


if __name__ == "__main__":
    pass
    clear_screen_shot(4)
