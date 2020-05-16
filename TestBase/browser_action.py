# -*- coding:utf-8 -*-
from selenium import webdriver
from Common.com_func import project_path, log, mkdir
from Common.test_func import send_DD_for_FXC
from selenium.webdriver import DesiredCapabilities
from Env import env_config as cfg
from selenium.common.exceptions import TimeoutException
from Config import global_var as gv
import time
from Tools.mongodb import MongoGridFS


# 获取 浏览器驱动函数（闭包）目的：延迟执行该函数
def get_driver_func(pro_name, browser_name, remote=False):
    def browser_driver():
        try:
            if remote:
                if browser_name == "Firefox":
                    return webdriver.Remote(command_executor='http://' + cfg.GRID_REMOTE_ADDR + '/wd/hub',
                                            desired_capabilities=DesiredCapabilities.FIREFOX)
                if browser_name == "Chrome":
                    return webdriver.Remote(command_executor='http://' + cfg.GRID_REMOTE_ADDR + '/wd/hub',
                                            desired_capabilities=DesiredCapabilities.CHROME)
            else:
                if browser_name == "Firefox":
                    return webdriver.Firefox(service_log_path=None)
                if browser_name == "Chrome":
                    return webdriver.Chrome()
        except Exception as e:
            log.error(("显示异常：" + str(e)))
            if "Failed to establish a new connection" in str(e):
                send_DD_for_FXC(title=pro_name, text="#### Selenium Hub 服务未启动 ！")
                raise Exception("Selenium Hub 服务未启动")
            elif "Error forwarding the new session" in str(e):
                send_DD_for_FXC(title=pro_name, text="#### Selenium Node 服务未启动 ！")
                raise Exception("Selenium Node 服务未启动")
            else:
                raise Exception("Selenium 服务的其他异常")
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

    def screenshot(self, image_name, case_instance):
        """
         截 图、保 存 mongo、记录图片ID
        :param image_name: 图片名称
        :param case_instance: 测试类实例对象
        :return:
        """
        current_test_path = cfg.SCREENSHOTS_DIR + case_instance.pro_name + "/" + case_instance.class_method_path  # ../类名/方法名/
        mkdir(current_test_path)
        self.driver.save_screenshot(current_test_path + image_name)
        mgf = MongoGridFS()
        files_id = mgf.upload_file(img_file_full=current_test_path + image_name)
        case_instance.screen_shot_id_list.append(files_id)

    def assert_content_and_screenshot(self, image_name, case_instance, content, time_out, error_msg):
        """
        断言内容是否存在、同时截屏
        :param image_name: 图片名称
        :param case_instance: 测试类实例对象
        :param content: 需要轮询的内容
        :param time_out: 轮询内容的超时时间
        :param error_msg: 断言失败后的 错误提示
        :return:
        """
        is_exist = True
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= time_out:
                is_exist = False
                break
        self.screenshot(image_name, case_instance)
        case_instance.assertTrue(is_exist, error_msg)


if __name__ == "__main__":
    print(project_path())

