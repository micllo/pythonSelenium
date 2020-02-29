# -*- coding:utf-8 -*-
from TestCasesRun.run_suite2 import sync_run_case2
from concurrent.futures import ThreadPoolExecutor
from Config import config as cfg
import sys, os
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
    pool.submit(sync_run_case2, browser_name=browser_name, thread_num=thread_num, remote=True)


def clear_reports_logs(clear_time):
    """
    删除一周前生成的报告和日志
      -mmin +1 -> 表示1分钟前的
      -mtime +1 -> 表示1天前的
    :param clear_time:
    :return:
    """
    rm_log_cmd = "find '" + cfg.LOGS_PATH + "' -name '*.log' -mmin +" + str(clear_time) + " -type f -exec rm -rf {} \\;"
    rm_report_cmd = "find '" + cfg.REPORTS_PATH + "history' -name '*.html' -mmin +" + str(clear_time) + \
                    " -type f -exec rm -rf {} \\;"
    print(rm_log_cmd)
    print(rm_report_cmd)
    os.system(rm_log_cmd)
    os.system(rm_report_cmd)


if __name__ == "__main__":
    pass
    clear_reports_logs(10)