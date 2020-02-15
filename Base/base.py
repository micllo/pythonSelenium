from Common.log import FrameLog
from selenium import webdriver
import time


# 获取浏览器驱动列表（ 同时开启浏览器 ）
def get_browser_driver_list(browser_list):
    driver_list = []
    for browser_name in browser_list:
        if browser_name == "Firefox":
            driver_list.append(webdriver.Firefox(service_log_path=None))
        if browser_name == "Chrome":
            driver_list.append(webdriver.Chrome())
    return driver_list


# 获取浏览器驱动
def get_browser_driver(browser_name):
    if browser_name == "Firefox":
        return webdriver.Firefox(service_log_path=None)
    if browser_name == "Chrome":
        return webdriver.Chrome()
    return print("浏览器驱动名称不正确")


# 获取 浏览器驱动函数（闭包）目的：延迟执行该函数
def get_driver_func(browser_name):
    def browser_driver():
        if browser_name == "Firefox":
            return webdriver.Firefox(service_log_path=None)
        if browser_name == "Chrome":
            return webdriver.Chrome()
    return browser_driver


class Base(object):

    def __init__(self, driver):
        self.driver = driver
        self.log = FrameLog().log()

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

    def test(self):
        print("hi")


if __name__ == "__main__":

  pass
