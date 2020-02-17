# -*- coding:utf-8 -*-
from TestCasesRun.run_suite2 import sync_run_case2
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append("./")

"""
api 服务底层的业务逻辑
"""


def sync_run_case_exec(browser_name):
    """
    同时执行不同的用例
    :param browser_name: Chrome、Firefox
    :return:
    """
    pool = ThreadPoolExecutor(1)
    pool.submit(sync_run_case2, browser_name=browser_name, thread_num=2, remote=False)
