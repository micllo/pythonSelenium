import time
from TestCases.train_test import TrainTest
from TestCases.demo_test import DemoTest
from Base.base_unit import ParaCase
from concurrent.futures import ThreadPoolExecutor
from Common import global_var as gl
from unittest.suite import _isnotsuite
from types import MethodType
from Common.function import project_path
import unittest
from Common.log import FrameLog
from Common.genReport import HTMLTestRunner


"""
 [ 动态修改 suite.py 文件中 TestSuite 类中的 run 方法 ]

 def run(self, result, debug=False) 
    ......... 
    for index, test in enumerate(self):
        .........
        test(result) 
        .........

 self ：
 -> 表示 suite 实例对象（包含了所有的测试用例实例，即继承了'unittest.TestCase'的子类的实例对象 test_instance ）
 <unittest.suite.TestSuite tests=[<TestCases.train_test.TrainTest testMethod=test_01>, 
                                  <TestCases.train_test.TrainTest testMethod=test_02>, 
                                  <TestCases.train_test.TrainTest testMethod=test_baidu>]>

 result:
 -> 表示 result.py 文件中的 TestResult 类的 实例对象

 test(result) ：等同于 test_instance(result)
 -> 表示 调用'unittest.TestCase'中的__call__方法执行该类中的 run 方法
 -> 理解：实例对象'test'通过'__call__'方法将自己变成一个函数来调用

"""


def run_test_custom(self, test, result, debug, index):
    """
    多线程中执行的内容
      1.需要为实例对象'suite'<TestSuite>动态添加该方法
      2.目的：供多线程中调用
    """
    if not debug:
        test(result)
    else:
        test.debug()

    if self._cleanup:
        self._removeTestAtIndex(index)
    return "\n" + str(test) + " ++++++++当前用例执行完毕+++++++\n"


def show_result_custom(res):
    """
    多线程回调函数
      1.需要为实例对象'suite'<TestSuite>动态添加该方法
      2.目的：供多线程中调用
    """
    result = res.result()
    FrameLog().log().info(result)


def new_run(self, result, debug=False):
    """
    动态修改'suite.py'文件中'TestSuite'类中的'run'方法
      1.为实例对象'suite'<TestSuite>动态修改实例方法'run'
      2.目的：启用多线程来执行case
    """
    topLevel = False
    if getattr(result, '_testRunEntered', False) is False:
        result._testRunEntered = topLevel = True

    # 多线程执行测试
    pool = ThreadPoolExecutor(gl.THREAD_NUM)
    for index, test in enumerate(self):
        if result.shouldStop:
            break

        if _isnotsuite(test):
            self._tearDownPreviousClass(test, result)
            self._handleModuleFixture(test, result)
            self._handleClassSetUp(test, result)
            result._previousTestClass = test.__class__

            if (getattr(test.__class__, '_classSetupFailed', False) or
                    getattr(result, '_moduleSetUpFailed', False)):
                continue

        pool.submit(run_test_custom, self, test, result, debug, index).add_done_callback(show_result_custom)

    # 等待所有线程执行完毕
    pool.shutdown()

    print("线程全部执行完毕")

    if topLevel:
        self._tearDownPreviousClass(None, result)
        self._handleModuleTearDown(result)
        result._testRunEntered = False
    return result


def sync_run_case2(browser_name, thread_num=5):
    """
    同时执行不同用例（ 通过动态修改'suite.py'文件中'TestSuite'类中的'run'方法，使得每个线程中的结果都可以记录到测试报告中 ）
    :param browser_name: 浏览器名称
    :param thread_num: 线程数

    【 备 注 】
     开启浏览器操作（每个用例执行一次）：在每个'测试类'的 setUp 方法中执行 ( 继承 ParaCase 父类 )
     关闭浏览器操作（每个用例执行一次）：在每个'测试类'的 tearDown 方法中执行 ( 继承 ParaCase 父类 )
    """

    gl.BROWSER_NAME = browser_name
    gl.THREAD_NUM = thread_num

    # 配置需要执行的'测试类'列表
    test_class_list = [TrainTest, DemoTest]

    # 将'测试类'中的所有'测试方法'添加到 suite 对象中
    suite = ParaCase.parametrize(test_class_list=test_class_list)

    # 为实例对象'suite'<TestSuite>动态添加两个方法'run_test_custom'、'show_result_custom'（ 目的：供多线程中调用 ）
    suite.run_test_custom = MethodType(run_test_custom, suite)
    suite.show_result_custom = MethodType(show_result_custom, suite)

    # 为实例对象'suite'<TestSuite>动态修改实例方法'run'（ 目的：启用多线程来执行case ）
    suite.run = MethodType(new_run, suite)

    print("实例对象suite是否存在'run_test_custom'方法：" + str(hasattr(suite, "run_test_custom")))
    print("实例对象suite是否存在'show_result_custom'方法：" + str(hasattr(suite, "show_result_custom")))
    print("实例对象suite是否存在'run'方法：" + str(hasattr(suite, "run")))
    print(suite)
    print(suite.__class__)
    print(suite.__class__.__base__)
    print("+++++++++++++++++++++++++++++++++++")

    # 运行内容再控制台显示(verbosity:表示控制台显示内容的等级，大于1时显示的内容更具体)
    # runner = unittest.TextTestRunner(verbosity=1)
    # test_result = runner.run(suite)

    # 运行内容在报告中显示
    now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
    report_path = project_path() + "Reports/" + now + '.html'
    with open(report_path, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title='UI自动化测试报告', description='详细测试用例结果', tester="费晓春", verbosity=2)
        test_result = runner.run(suite)

    # log_console = FrameLog().log()
    # log_console.info(test_result)
    # log_console.info("执行总数：" + str(test_result.error_count + test_result.success_count + test_result.failure_count))
    # log_console.info("执行的用例列表：" + str(test_result.result))
    # log_console.info("错误数：" + str(test_result.error_count))
    # log_console.info("错误的用例列表：" + str(test_result.errors))
    # log_console.info("失败数：" + str(test_result.failure_count))
    # log_console.info("失败的用例列表：" + str(test_result.failures))
    # log_console.info("成功数：" + str(test_result.success_count))
    # log_console.info("成功的用例列表：" + str([success[1] for success in test_result.result if success[0] == 0]))
    # log_console.info("每个用例的时间：开始时间、结束时间、运行时间：")


if __name__ == "__main__":

    # "Firefox"、"Chrome"
    sync_run_case2(browser_name="Chrome", thread_num=2)
    pass

