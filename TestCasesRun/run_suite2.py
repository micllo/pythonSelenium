# -*- coding:utf-8 -*-
from TestCases.train_test import TrainTest
from TestCases.demo_test import DemoTest
from Base.test_case_unit import ParaCase
from concurrent.futures import ThreadPoolExecutor
from unittest.suite import _isnotsuite
from types import MethodType
from Tools.log import FrameLog
from Common.test_func import generate_report
from Common.test_func import send_warning_after_test


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
    pool = ThreadPoolExecutor(self.thread_num)
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


def sync_run_case2(browser_name, thread_num=2, remote=False):
    """
    同时执行不同用例（ 通过动态修改'suite.py'文件中'TestSuite'类中的'run'方法，使得每个线程中的结果都可以记录到测试报告中 ）
    :param browser_name: 浏览器名称
    :param thread_num: 线程数
    :param remote: 是否远程执行
    【 备 注 】
     suite 实例对象（包含了所有的测试用例实例，即继承了'unittest.TestCase'的子类的实例对象 test_instance ）
     开启浏览器操作（每个用例执行一次）：在每个'测试类'的 setUp 方法中执行 ( 继承 ParaCase 父类 )
     关闭浏览器操作（每个用例执行一次）：在每个'测试类'的 tearDown 方法中执行 ( 继承 ParaCase 父类 )

     【 保 存 截 屏 图 片 ID 的 逻 辑 】
      1.为实例对象'suite'<TestSuite>动态添加一个属性'screen_shot_id_dict' -> screenshot_id_dict = {}
      2.每个测试方法中将所有截屏ID的保存入'screen_shot_id_list' -> screenshot_id_list = ['aaa', 'bbb', 'ccc']
      3.每个测试方法最后返回'screen_shot_id_list'
      4.实例对象'suite'在重写的'new_run'方法中将'screenshot_id_list'添加入'screenshot_id_dict'
      5.screen_shot_id_dict = { "类名.方法名":['aaa', 'bbb'], "类名.方法名":['cccc'] }


      screen_shot_id_list: [ObjectId('5e5e0166299e6d3a9f80facc'), ObjectId('5e5e0170299e6d3a9f80fad4'), ObjectId('5e5e0175299e6d3a9f80fad9')]

    """

    # 配置需要执行的'测试类'列表
    # test_class_list = [DemoTest]
    test_class_list = [TrainTest, DemoTest]

    # 将'测试类'中的所有'测试方法'添加到 suite 对象中（每个'测试类'实例对象包含一个'测试方法'）
    suite = ParaCase.parametrize(test_class_list=test_class_list, browser_name=browser_name, remote=remote)

    # 为实例对象'suite'<TestSuite>动态添加一个属性'thread_num'（目的：控制多线程数量）
    setattr(suite, "thread_num", thread_num)

    # 为实例对象'suite'<TestSuite>动态添加两个方法'run_test_custom'、'show_result_custom'（ 目的：供多线程中调用 ）
    suite.run_test_custom = MethodType(run_test_custom, suite)
    suite.show_result_custom = MethodType(show_result_custom, suite)

    # 为实例对象'suite'<TestSuite>动态修改实例方法'run'（ 目的：启用多线程来执行case ）
    suite.run = MethodType(new_run, suite)

    # 生成测试报告
    test_result, current_report_file = generate_report(suite=suite, title='UI自动化测试报告', description='详细测试用例结果',
                                                       tester="FXC", verbosity=2)
    # 测试后发送预警
    send_warning_after_test(test_result, current_report_file)


if __name__ == "__main__":

    # "Firefox"、"Chrome"
    sync_run_case2(browser_name="Chrome", thread_num=3, remote=False)
    # sync_run_case2(browser_name="Firefox", thread_num=3, remote=True)


