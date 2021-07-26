# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.select import Select  # 下拉框
from selenium.webdriver.common.action_chains import ActionChains  # 连续动作（拖动、鼠标操作、JS操作）
from selenium.webdriver.common.keys import Keys  # 键盘操作
from Common.com_func import project_path, log, mkdir
from Common.test_func import send_DD_for_FXC
from selenium.webdriver import DesiredCapabilities
from Env import env_config as cfg
from selenium.common.exceptions import TimeoutException
from Config import global_var as gv
import time
from Tools.mongodb import MongoGridFS


def get_driver_func(pro_name, browser_name, remote=False):
    """
     获取 浏览器驱动函数（闭包）目的：延迟执行该函数
    :param pro_name:
    :param browser_name:
    :param remote:
    :return:
    """
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
                    return webdriver.Firefox(service_log_path=None, executable_path=cfg.FIREFOX_DRIVER_FILE).get()
                if browser_name == "Chrome":
                    return webdriver.Chrome(executable_path=cfg.CHROME_DRIVER_FILE)
        except Exception as e:
            log.error(("显示异常：" + str(e)))
            if "Failed to establish a new connection" in str(e):
                error_msg = "Selenium Hub 服务未启动"
            elif "Error forwarding the new session" in str(e):
                error_msg = "Selenium Node 服务未启动 ( " + browser_name + " )"
            else:
                error_msg = "启动 Selenium 服务的其他异常情况"
            send_DD_for_FXC(title=pro_name, text="#### " + error_msg + "")
            raise Exception(error_msg)
    return browser_driver


class Base(object):

    def __init__(self, case_instance):
        self.case_instance = case_instance  # 测试用例的实例对象
        self.driver = case_instance.driver
        self.log = log

    def high_light(self, ele):
        self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele, "border:2px solid red;")

    def find_ele(self, by, value, hl=True):
        try:
            self.log.info("通过" + by + "定位，元素是 " + value)
            ele = self.driver.find_element(by, value)
            # ele = WebDriverWait(self.driver, time_out).until(self.driver.find_element(by, value))
            if hl:
                self.high_light(ele)
            return ele
        except:
            raise Exception(value + " 元素定位失败！")

    def click(self, by, value):
        self.find_ele(by, value).click()

    def send_key(self, by, value, content):
        self.find_ele(by, value).send_key(content)

    def js(self, js_str):
        self.driver.execute_script(js_str)

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

    # 下拉框选择操作
    def select_action(self, select_ele, option_value):
        """
        :param select_ele:  下拉框元素
        :param option_value: 选项的value属性值
        """
        Select(select_ele).select_by_value(option_value)
        time.sleep(2)

    # 动作链 生成器
    def action_chains(self):
        ac = ActionChains(self.driver)
        yield ac
        ac.perform()

    # 鼠标悬停
    def move_to_ele(self, ele):
        for ac in self.action_chains():
            ac.move_to_element(ele)

    # 双击
    def double_click(self, ele):
        for ac in self.action_chains():
            ac.double_click(ele)

    # 拖拽
    def drag_and_drop(self, source_ele, target_ele):
        for ac in self.action_chains():
            ac.drag_and_drop(source=source_ele, target=target_ele)  # 拖拽
            # ac.click_and_hold(source_ele)   # 鼠标按压
            # ac.move_to_element(target_ele)  # 鼠标滑动
            # ac.release()  # 鼠标释放

    # 键盘操作
    def keyboard_action(self, key_action):
        for ac in self.action_chains():
            ac.send_keys(key_action)  # 发送某个键到当前焦点的元素

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

    def screenshot(self, image_name):
        """
         截 图、保 存 mongo、记录图片ID
        :param image_name: 图片名称

            < 截屏方法 >
                save_screenshot()
                get_screenshot_as_file()    保存的是文件图片
                get_screenshot_as_base64()  保存的是base64编码，供报告页面展示
                get_screenshot_as_png()     保存的是二进制数据，很少用
        :return:

        【 使 用 case_instance 逻 辑 】
        1.若'Base类的子类实例对象'调用该方法（在 page_object 中使用）：则使用该实例对象本身的 self.case_instance 属性（测试用例实例对象）
        2.若'Base类'调用该方法（在 test_case 中使用）：则使用该 self 测试用例实例对象本身
        3.由于'Base'类和'测试用例类'都含有'driver'属性，所以不影响self.driver的使用
        """
        # 判断当前的'实例对象'是否为'Base'类型（或其子类）
        case_instance = isinstance(self, Base) and self.case_instance or self
        # 获取当前测试用例的路径 -> ../类名/方法名/
        current_test_path = cfg.SCREENSHOTS_DIR + case_instance.pro_name + "/" + case_instance.class_method_path
        mkdir(current_test_path)
        self.driver.save_screenshot(current_test_path + image_name)
        mgf = MongoGridFS()
        files_id = mgf.upload_file(img_file_full=current_test_path + image_name)
        case_instance.screen_shot_id_list.append(files_id)

    def assert_content_and_screenshot(self, image_name, content, error_msg):
        """
        断言内容是否存在、同时截屏
        :param image_name: 图片名称
        :param content: 需要轮询的内容
        :param error_msg: 断言失败后的 错误提示
        :return:
        """
        is_exist = True
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= gv.POLLING_CONTENT_TIME_OUT:
                is_exist = False
                break
        self.screenshot(image_name)
        self.case_instance.assertTrue(is_exist, error_msg)


if __name__ == "__main__":
    print(project_path())


