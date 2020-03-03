# -*- coding:utf-8 -*-
import unittest
import time
from TestCases.train_test import TrainTest
from Base.test_case_unit import ParaCase
from concurrent.futures import ThreadPoolExecutor
from Tools.log import FrameLog


def run_test(test_instence):
    """
    多线程中执行的内容
    :param test_instence:  实例对象 ->  test_02 (TestCases.TrainTest.LoginTest)
    :param browser_name:   浏览器名称
    :return:
    """
    suite = unittest.TestSuite()
    suite.addTest(test_instence)
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)
    test_instence.log.info(str(test_instence) + " 用 例 执 行 完 毕 ！")
    return str(test_instence) + " 用 例 执 行 完 毕 ！"


def run_result(res):
    """
    多线程回调函数
    :param res:  ->  pool.submit(run_test, None, class_test_case)
    :return:
    """
    result = res.result()
    FrameLog().log().info(result)


def sync_run_case(browser_name, thread_num=2, remote=False):
    """
    同时执行不同用例（ 由于每个线程中执行的用例会单独配置测试结果，所以测试结果只能打印在控制台 ）
    :param browser_name: 浏览器名称
    :param thread_num: 线程数
    :param remote: 是否远程执行
    :return:

    【 备 注 】
     开启浏览器操作（每个用例执行一次）：在每个'测试类'的 setUp 方法中执行 ( 继承 ParaCase 父类 )
     关闭浏览器操作（每个用例执行一次）：在每个'测试类'的 tearDown 方法中执行 ( 继承 ParaCase 父类 )
    """

    # 配置需要执行的'测试类'列表
    test_class_list = [TrainTest]

    # 解析'测试类'列表
    suite = ParaCase.parametrize(test_class_list=test_class_list, browser_name=browser_name, remote=remote)

    # 获取'测试类的实例对象'列表
    test_instence_list = suite._tests

    # 多线程执行测试
    pool = ThreadPoolExecutor(thread_num)
    for test_instence in test_instence_list:
        # 多线程调用函数：res = run_test(test_instence)
        # res = pool.submit(run_test, test_instence)
        # 多线程回调函数：run_result(res)
        # res.add_done_callback(run_result)
        # 简 写 ( 目的：哪个线程执行完毕了，可马上执行回调函数 )
        pool.submit(run_test, test_instence).add_done_callback(run_result)
        time.sleep(1)
    # 等待所有线程执行完毕
    pool.shutdown()


if __name__ == "__main__":

    # "Firefox"、"Chrome"
    sync_run_case(browser_name="Chrome", thread_num=2, remote=False)



