from Common.HTMLTestReport import HTMLTestRunner
from Config import config as cfg
import time
from Common.log import FrameLog


def generate_report(suite, title, description, tester, verbosity=1):
    """
    生 成 测 试 报 告
    :param suite: suite 实例对象（包含了所有的测试用例实例，即继承了'unittest.TestCase'的子类的实例对象 test_instance ）
    :param title:
    :param description:
    :param tester:
    :param verbosity: 结果显示的详细程度
    :return:
    """
    print("实例对象suite是否存在'run_test_custom'方法：" + str(hasattr(suite, "run_test_custom")))
    print("实例对象suite是否存在'show_result_custom'方法：" + str(hasattr(suite, "show_result_custom")))
    print("实例对象suite是否存在'run'方法：" + str(hasattr(suite, "run")))
    print(suite)
    print(suite.__class__)
    print(suite.__class__.__base__)
    print("+++++++++++++++++++++++++++++++++++")

    now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
    report_path = cfg.REPORTS_PATH + now + '.html'
    with open(report_path, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title=title, description=description, tester=tester, verbosity=verbosity)
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
