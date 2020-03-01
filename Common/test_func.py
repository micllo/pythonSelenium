# -*- coding:utf-8 -*-
from Common.HTMLTestReport import HTMLTestRunner
from Config import config as cfg
import time
import os
from Common.function import mkdir, log
from Common.function import log, send_mail
from Config import global_var as gv
import requests
import json


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
    history_report_file = history_report_path + current_report_name
    with open(history_report_file, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title=title, description=description, tester=tester, verbosity=verbosity)
        test_result = runner.run(suite)

    # 将最新报告替换../logs/下的report.html
    res = os.system("cp " + history_report_file + " " + cfg.REPORTS_PATH + " && "
                    "mv " + cfg.REPORTS_PATH + current_report_name + " " + cfg.REPORTS_PATH + "report.html")
    if res != 0:
        log.error("测试报告替换操作有误！")

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
    return test_result, history_report_file


def send_warning_after_test(test_result, report_file):
    """
        测 试 后 发 送 预 警 （ 邮件、钉钉 ）
        (1)有'失败'的，则标记为'失败'
        (2)无'失败'、有'错误'的，则标记为'错误'
        (3)无'失败'、无'错误'的，则标记为'None'
        :param test_result:
        :param report_file:
        :return:
    """
    report_name = report_file.split("/")[-1]
    error_type = (test_result.failure_count > 0 and "失败" or (test_result.error_count > 0 and "错误" or None))
    if error_type:
        send_mail_after_test(error_type=error_type, report_name=report_name, report_file=report_file)
        is_at_all = (error_type == "失败" and True or False)
        send_DD_after_test(error_type=error_type, report_name=report_name, is_at_all=is_at_all)


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

    备注：若要@某个人，则需要在'text'中@其手机号
    （1）at_text -> \n\n@138xxxxxx @139xxxxxx
    """

    at_all = "true"
    at_mobiles = []
    at_text = ""
    if not is_at_all:
        at_all = "false"
        at_mobiles = cfg.DD_AT_PHONE.split(",")
        at_text += "\n\n"
        at_mobile_text = ""
        for mobile in at_mobiles:
            at_mobile_text += "@" + mobile + " "
        at_text += at_mobile_text

    text_msg = {"title": "UI自动化监控"}
    text_msg["text"] = "#### 在'" + report_name + "'测试报告中 存在'" + error_type + \
                       "'的用例\n\n ***测试报告地址***\n" + cfg.TEST_REPORT_URL + at_text
    data = {"msgtype": "markdown"}
    data["markdown"] = text_msg
    data["at"] = {"atMobiles": at_mobiles, "isAtAll": at_all}
    dd_url = gv.DD_BASE_URL + cfg.DD_MONITOR
    log.info(data)
    headers = {'Content-Type': 'application/json'}
    try:
        requests.post(url=dd_url, data=json.dumps(data), headers=headers)
    except Exception as e:
        log.error("钉钉发送失败")
        log.error(e)


if __name__ == "__main__":
    send_DD_after_test("失败", "报告名称", False)