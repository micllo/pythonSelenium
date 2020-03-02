# -*- coding:utf-8 -*-
from selenium import webdriver
from Common.function import project_path, get_config_ini, log, mkdir, send_DD
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from Config import config as cfg
from selenium.common.exceptions import TimeoutException
from Config import global_var as gv
import time
from Common.mongodb import MongoGridFS

import os, sys


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

    def high_light(self, ele):
        self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele, "border:2px solid red;")

    def find_ele(self, *args):
        try:
            self.log.info("通过" + args[0] + "定位，元素是 " + args[1])
            ele = self.driver.find_element(*args)
            # ele = WebDriverWait(self.driver, time_out).until(self.driver.find_element(*args))
            self.high_light(ele)
            return ele
        except:
            raise Exception(args[1] + " 元素定位失败！")

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

    # 关闭所有窗口
    def quit(self):
        self.driver.quit()

    # 关闭当前窗口
    def close(self):
        self.driver.close()

    # 截图并保存入mongo
    def screenshot(self, class_method_path, image_name):
        # log.info(self)
        # log.info(self.__class__)
        current_test_path = cfg.SCREENSHOTS_PATH + class_method_path
        mkdir(current_test_path)
        self.driver.save_screenshot(current_test_path + image_name)
        mgf = MongoGridFS()
        files_id = mgf.upload_file(img_file_full=current_test_path + image_name)
        return files_id

    # 打开一个新窗口，并将句柄切到新窗口，返回原窗口句柄
    def open_new_window(self):
        old_handle = self.driver.current_window_handle
        self.driver.execute_script('window.open("https://www.baidu.com");')
        for handle in self.driver.window_handles:
            if handle != old_handle:
                self.driver.switch_to.window(handle)
        return old_handle

    # 当页面加载超时后，停止加载（为了可以继续后续driver操作）
    def get_page_with_time_out(self, url, time_out):
        try:
            self.driver.set_page_load_timeout(time_out)
            self.driver.get(url)
        except TimeoutException:
            log.error("页面'" + url + "'加载 " + str(time_out) + " 秒超时了!")
            self.driver.execute_script('window.stop()')
        finally:
            self.driver.set_page_load_timeout(gv.PAGE_LOAD_TIME)  # 还原默认的加载页面超时时间

    # 判断页面内容是否存在
    def content_is_exist(self, content, time_out):
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= time_out:
                return False
        return True

    # 判断页面内容是否存在，同时截屏
    def content_is_exist_with_screenshot(self, content, time_out, class_method_path, image_name):
        is_exist = True
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= time_out:
                is_exist = False
                break
        self.screenshot(class_method_path, image_name)
        return is_exist



if __name__ == "__main__":
    print(project_path())

