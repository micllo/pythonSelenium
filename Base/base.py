# -*- coding:utf-8 -*-
from selenium import webdriver
from Common.function import project_path, get_config_ini, log
from selenium.webdriver import DesiredCapabilities
from Config import config as cfg
import time
import os


# 获取浏览器驱动列表（ 同时开启浏览器 ）
def get_browser_driver_list(browser_list, remote=False):
    driver_list = []
    if remote:
        for browser_name in browser_list:
            if browser_name == "Firefox":
                driver_list.append(webdriver.Remote(command_executor='http://' + get_config_ini("remote_ip", "ip_port")
                                  + '/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX))
            if browser_name == "Chrome":
                driver_list.append(webdriver.Remote(command_executor='http://' + get_config_ini("remote_ip", "ip_port")
                                    + '/wd/hub', desired_capabilities=DesiredCapabilities.CHROME))
    else:
        for browser_name in browser_list:
            if browser_name == "Firefox":
                driver_list.append(webdriver.Firefox(service_log_path=None))
            if browser_name == "Chrome":
                driver_list.append(webdriver.Chrome())
    return driver_list


# # 获取浏览器驱动
# def get_browser_driver(browser_name, remote=False):
#     if remote:
#         if browser_name == "Firefox":
#             return webdriver.Remote(command_executor='http://' + get_config_ini("remote_ip", "ip_port") + '/wd/hub',
#                                     desired_capabilities=DesiredCapabilities.FIREFOX)
#         if browser_name == "Chrome":
#             return webdriver.Remote(command_executor='http://' + get_config_ini("remote_ip", "ip_port") + '/wd/hub',
#                                     desired_capabilities=DesiredCapabilities.CHROME)
#     else:
#         if browser_name == "Firefox":
#             return webdriver.Firefox(service_log_path=None)
#         if browser_name == "Chrome":
#             return webdriver.Chrome()
#     return print("浏览器驱动名称不正确")
#

# 获取 浏览器驱动函数（闭包）目的：延迟执行该函数
def get_driver_func(browser_name, remote=False):
    def browser_driver():
        try:
            if remote:
                if browser_name == "Firefox":
                    return webdriver.Remote(
                        command_executor='http://' + get_config_ini("remote_ip", "ip_port") + '/wd/hub',
                        desired_capabilities=DesiredCapabilities.FIREFOX)
                if browser_name == "Chrome":
                    return webdriver.Remote(
                        command_executor='http://' + get_config_ini("remote_ip", "ip_port") + '/wd/hub',
                        desired_capabilities=DesiredCapabilities.CHROME)
            else:
                if browser_name == "Firefox":
                    return webdriver.Firefox(service_log_path=None)
                if browser_name == "Chrome":
                    return webdriver.Chrome()
        except Exception as e:
            log.error(("显示异常：" + str(e)))
            log.error("远程浏览器监听未开启！！！")
            raise Exception("远程浏览器监听未开启")
    return browser_driver


class Base(object):

    def __init__(self, driver):
        self.driver = driver
        self.log = log

    def find_ele(self, *args):
        try:
            # print(args)
            self.log.info("通过" + args[0] + "定位，元素是 " + args[1])
            return self.driver.find_element(*args)
        except:
            self.log.error("定位元素失败!")

    def click(self, *args):
        self.find_ele(*args).click()

    def send_key(self, *args, value):
        self.find_ele(*args).send_key(value)

    def js(self, str):
        self.driver.execute_script(str)

    def url(self):
        return self.driver.current_url

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def quit(self):
        self.driver.quit()

    def screenshot(self, image_name):
        self.driver.save_screenshot(cfg.SCREENSHOTS_PATH + image_name)

    def test(self):
        print("hi")


if __name__ == "__main__":
    print(project_path())

