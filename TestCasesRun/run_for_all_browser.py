import unittest
from Common.genReport import HTMLTestRunner
import time
from Common.function import project_path, MyThread
from TestCases.train_test import TrainTest
from TestCases.demo_test import DemoTest
from Base.base_unit import ParaCase
from Base.base import get_browser_driver_list
from Common.log import FrameLog


def run_suite(driver, test_class_list):
    """
    多线程中run方法实际执行的内容
    :param driver:
    :return:
    """
    # 将'测试类'中的所有'测试方法'添加到 suite 对象中
    suite = unittest.TestSuite()
    suite.addTest(ParaCase.parametrize(test_class_list=test_class_list, driver=driver))

    # 运行内容再控制台显示
    # suite = unittest.defaultTestLoader.discover(project_path() + "TestCases", pattern='Train*.py')
    # runner = unittest.TextTestRunner(verbosity=1)
    # test_result = runner.run(suite)
    # print("执行总数 testsRun：" + str(test_result.testsRun))
    # print("执行的用例列表：")
    # print("成功的用例列表：")
    # print("错误的用例列表（错误日志）errors：" + str(test_result.errors))
    # print("失败的用例列表（失败日志）failures：" + str(test_result.failures))
    # print("每个用例的时间：开始时间、结束时间、运行时间：")
    # print()

    # 运行内容再报告中显示
    now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
    report_path = project_path() + "Reports/" + now + '.html'
    with open(report_path, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='详细测试用例结果', tester="费晓春", verbosity=2)
        test_result = runner.run(suite)

    print(test_result)
    print("执行总数：" + str(test_result.error_count + test_result.success_count + test_result.failure_count))
    print("执行的用例列表：" + str(test_result.result))
    print("错误数：" + str(test_result.error_count))
    print("错误的用例列表：" + str(test_result.errors))
    print("失败数：" + str(test_result.failure_count))
    print("失败的用例列表：" + str(test_result.failures))
    print("成功数：" + str(test_result.success_count))
    print("成功的用例列表：" + str([success[1] for success in test_result.result if success[0] == 0]))
    print("每个用例的时间：开始时间、结束时间、运行时间：")

    for n, t, o, e in test_result.result:
        print(o)
        print("++++++++++")


def run_all_case_for_all_browser(browser_list, test_class_list):
    """
    使用不同浏览器分别同时执行所有用例（目的：浏览器兼容性测试）
    :param test_class_list: 需要执行的'测试类'列表
    :param browser_list: 需要执行的浏览器
    :return:

    【 备 注 】
     开启浏览器操作（ 仅执行一次 ）：在当前流程中执行
     关闭浏览器操作（ 仅执行一次 ）：在当前流程中执行
    """

    """
      由于 为了使所有用例都以指定的浏览器进行测试 
      因此 需要删除所有测试类中的启动浏览器和关闭浏览器的操作

      方式：通过反射来删除'ParaCase'类中的'setUp'和'tearDown'方法
    """
    delattr(ParaCase, "setUp")
    delattr(ParaCase, "tearDown")

    # 获取浏览器驱动列表（ 同时开启浏览器 ）
    driver_list = get_browser_driver_list(browser_list)

    # 执行测试
    th_list = []
    for i in range(len(driver_list)):
        print(driver_list[i])
        th = MyThread(func=run_suite, driver=driver_list[i], test_class_list=test_class_list)
        th_list.append(th)
        th.start()
        time.sleep(2)

    # 等待线程结束
    for i in range(len(th_list)):
        th_list[i].join()

    # 关闭浏览器
    for i in range(len(driver_list)):
        driver_list[i].quit()


if __name__ == "__main__":

    # run_all_case_for_all_browser(browser_list=["Firefox"], test_class_list=[TrainTest, DemoTest])
    run_all_case_for_all_browser(browser_list=["Chrome"], test_class_list=[TrainTest, DemoTest])
    # run_all_case_for_all_browser(browser_list=["Firefox", "Chrome"], test_class_list=[TrainTest, DemoTest])

