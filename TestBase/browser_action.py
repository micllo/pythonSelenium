# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait    # 智能等待
from selenium.webdriver.support.select import Select  # 下拉框
from selenium.webdriver.common.action_chains import ActionChains  # 连续动作（拖动、鼠标操作、JS操作）
from Common.com_func import project_path, log, mkdir
from Common.test_func import send_DD_for_FXC
from selenium.webdriver import DesiredCapabilities
from Env import env_config as cfg
from selenium.common.exceptions import TimeoutException
from Config import global_var as gv
import time
from Tools.mongodb import MongoGridFS
from Tools.decorator_tools import get_action_chains


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

    # 自定义条件等待（ 非找元素的等待，不同与 implicitly_wait ）
    def condition_wait(self, condition, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(condition)
        except TimeoutException:
            raise TimeoutException("自定义条件等待超时！")

    # 单元素定位
    def find_ele(self, by, value, hl=True):
        try:
            self.log.info("通过" + by + "定位，元素是 " + value)
            ele = self.driver.find_element(by, value)
            if hl:
                self.high_light(ele)
            return ele
        except:
            raise Exception(value + " 单元素定位失败！")

    # 多元素定位
    def find_eles(self, by, value):
        ele_list = self.driver.find_elements(by, value)
        if ele_list:
            return ele_list
        else:
            raise Exception("多元素定位失败！")

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

    """ ####################### 使用 switch_to 跳转 ####################### """

    # 操作 alert 弹框
    def action_alert(self, action):
        """
        :param action: 确定、取消
        """
        alert = self.driver.switch_to.alert
        time.sleep(2)
        if action == "accept":
            alert.accept()
        else:
            alert.dismiss()

    # 打开一个新窗口，并将句柄切到新窗口，返回原窗口句柄
    def open_new_window(self):
        old_handle = self.driver.current_window_handle
        self.driver.execute_script('window.open("https://www.baidu.com");')
        self.driver.switch_to.window(self.driver.window_handles[:-1])
        # for handle in self.driver.window_handles:
        #     if handle != old_handle:
        #         self.driver.switch_to.window(handle)
        return old_handle

    # 跳转 frame 框
    def action_frame(self):
        self.driver.switch_to.frame()            # 跳转至下一级frame
        self.driver.switch_to.default_content()  # 跳回原始页面
        self.driver.switch_to.parent_frame()     # 跳回上一级frame

    """ ####################### 使用 ActionChains 动作链 ####################### """

    def action_chains_yield(self):
        """
            动 作 链 生成器
            目的：每次使用动作链时，都需要新建动作链对象
            原因：若只使用一个动作链对象，每次perform()运行时都会将之前保存的动作都重新执行一遍
                 除非能保证一个用例中只使用一次动作链，且动作链中不能有其他操作步骤
        """
        action_chains = ActionChains(self.driver)
        yield action_chains
        action_chains.perform()

    # 鼠标悬停（不使用装饰器）
    def move_to_ele_demo(self, ele=None):
        ActionChains(self.driver).move_to_element(ele).perform()

    # 鼠标悬停
    @get_action_chains  # move_to_ele = get_ac(move_to_ele)
    def move_to_ele(self, action_chains=None, ele=None):
        action_chains.move_to_element(ele)

    # 双击
    @get_action_chains
    def double_click(self, action_chains=None, ele=None):
        action_chains.double_click(ele)

    # 拖拽
    @get_action_chains
    def drag_and_drop(self, action_chains=None, s_ele=None, t_ele=None):
        action_chains.drag_and_drop(source=s_ele, target=t_ele)  # 拖拽
        # action_chains.click_and_hold(source_ele)   # 鼠标按压
        # action_chains.move_to_element(target_ele)  # 鼠标滑动
        # action_chains.release()  # 鼠标释放

    # 键盘操作
    @get_action_chains
    def keyboard_action(self, action_chains=None, key_action=None):
        action_chains.send_keys(key_action)  # 发送某个键到当前焦点的元素

    """ ######################################################################## """

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


