# -*- coding:utf-8 -*-
from Common.HTMLTestReport import HTMLTestRunner
import time
import os
from Common.com_func import send_mail, mkdir, send_DD, log
from Config import config as cfg


def generate_report(suite, title, description, tester, verbosity=1):
    """
    生 成 测 试 报 告
    备注：每次生成的报告都存放在../logs/history/中，同时替换../logs/下的report.html
    :param suite: suite 实例对象（包含了所有的测试用例实例，即继承了'unittest.TestCase'的子类的实例对象 test_instance ）
    :param title:
    :param description:
    :param tester:
    :param verbosity: 结果显示的详细程度
    :return:
    """
    print("实例对象suite是否存在'thread_num'属性：" + str(hasattr(suite, "thread_num")))
    print("实例对象suite是否存在'screen_shot_id_dict'属性：" + str(hasattr(suite, "screen_shot_id_dict")))
    print("实例对象suite是否存在'run_test_custom'方法：" + str(hasattr(suite, "run_test_custom")))
    print("实例对象suite是否存在'show_result_custom'方法：" + str(hasattr(suite, "show_result_custom")))
    print("实例对象suite是否存在'run'方法：" + str(hasattr(suite, "run")))
    print(suite)
    print(suite.__class__)
    print(suite.__class__.__base__)
    print("+++++++++++++++++++++++++++++++++++")

    now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
    current_report_name = now + ".html"
    history_report_path = cfg.REPORTS_PATH + "history/"
    mkdir(history_report_path)
    current_report_file = history_report_path + current_report_name
    with open(current_report_file, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title=title, description=description, tester=tester, verbosity=verbosity)
        test_result = runner.run(suite)

    # 将最新报告替换../logs/下的report.html
    res = os.system("cp " + current_report_file + " " + cfg.REPORTS_PATH + " && "
                    "mv " + cfg.REPORTS_PATH + current_report_name + " " + cfg.REPORTS_PATH + "report.html")
    if res != 0:
        log.error("测试报告替换操作有误！")

    # log.info(test_result)
    # log.info("执行总数：" + str(test_result.error_count + test_result.success_count + test_result.failure_count))
    # log.info("执行的用例列表：" + str(test_result.result))
    # log.info("错误数：" + str(test_result.error_count))
    # log.info("错误的用例列表：" + str(test_result.errors))
    # log.info("失败数：" + str(test_result.failure_count))
    # log.info("失败的用例列表：" + str(test_result.failures))
    # log.info("成功数：" + str(test_result.success_count))
    # log.info("成功的用例列表：" + str([success[1] for success in test_result.result if success[0] == 0]))
    # log.info(suite.screen_shot_id_dict)
    return test_result, current_report_file


def send_warning_after_test(test_result, report_file):
    """
       测 试 后 发 送 预 警 （ 邮件、钉钉 ）
       :param test_result:
       :param report_file:
       :return:
       error_type 标识：
         (1)有'失败'的，则标记为'失败'
         (2)无'失败'、有'错误'的，则标记为'错误'
         (3)无'失败'、无'错误'的，则标记为'None'
    """
    report_name = report_file.split("/")[-1]
    error_type = (test_result.failure_count > 0 and "失败" or (test_result.error_count > 0 and "错误" or None))
    if error_type:
        send_mail_after_test(error_type=error_type, report_name=report_name, report_file=report_file)
        send_DD_after_test(error_type=error_type, report_name=report_name, is_at_all=(error_type == "失败" and True or False))


def send_mail_after_test(error_type, report_name, report_file):
    """
    测 试 后 发 送 邮 件
    :param error_type: "失败"、"错误"
    :param report_name:
    :param report_file:
    :return:
    """
    subject = "UI自动化测试'" + report_name.split(".")[-2] + "'存在'" + error_type + "'的用例"
    content = "在'" + report_name + "'测试报告中 存在'" + error_type + "'的用例\n测试报告地址： " + cfg.TEST_REPORT_URL
    send_mail(subject=subject, content=content, to_list=cfg.MAIL_LIST, attach_file=report_file)


def send_DD_after_test(error_type, report_name, is_at_all=False):
    """
    测 试 后 发 送 钉 钉
    :param error_type: "失败"、"错误"
    :param report_name:
    :param is_at_all:
    :return:

    """
    title = "[监控]UI自动化"
    text = "#### 在'" + report_name + "'测试报告中 存在'" + error_type + "'的用例\n\n ***测试报告地址***\n" + cfg.TEST_REPORT_URL
    send_DD(dd_group_id=cfg.DD_MONITOR_GROUP, title=title, text=text, at_phones=cfg.DD_AT_PHONES, is_at_all=is_at_all)


def send_DD_for_FXC(title, text):
    """
    发 送 钉 钉 to FXC
    :param title:
    :param text:
    :return:

    """
    title = "[监控]" + title
    send_DD(dd_group_id=cfg.DD_MONITOR_GROUP, title=title, text=text, at_phones=cfg.DD_AT_FXC, is_at_all=False)


def mongo_exception_send_DD(e, msg):
    """
    发现异常时钉钉通知
    :param e:
    :param msg:
    :return:
    """
    title = "[监控]'mongo'操作通知"
    text = "#### UI自动化测试'mongo'操作错误\n\n****操作方式：" + msg + "****\n\n****错误原因：" + str(e) + "****"
    send_DD(dd_group_id=cfg.DD_MONITOR_GROUP, title=title, text=text, at_phones=cfg.DD_AT_FXC, is_at_all=False)


if __name__ == "__main__":
    # send_DD_after_test("失败", "报告名称", False)
    pass


