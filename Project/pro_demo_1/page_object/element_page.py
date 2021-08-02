# -*- coding:utf-8 -*-
from TestBase.browser_action import Base
from TestBase.webdriver_package import *


class ElementPage(Base):

    """
        【 元 素 定 位 】
    """

    # 下拉框
    @property  # 将 方法 设置成 属性 的调用方式
    def select_ele(self):
        return self.find_ele(By.NAME, "select")

    # 鼠标悬停元素
    @property
    def hover_ele(self):
        return self.find_ele(By.XPATH, "//*[@id='action']/input[1]")

    # 双击元素
    @property
    def double_click_ele(self):
        return self.find_ele(By.XPATH, "//*[@id='action']/input[2]")

    # 拖拽 源元素(滑块)
    @property
    def move_source_ele(self):
        return self.find_ele(By.XPATH, "//*[@id='slider']/span[1]")

    # 拖拽 目标元素(最右侧的第一个元素)
    @property
    def move_target_ele(self):
        return self.find_ele(by=By.ID, value="slider_confirm", hl=False)

    # alert 弹框
    @property
    def alert_ele(self):
        return self.find_ele(by=By.CLASS_NAME, value="prompt")

    # 下单 按钮
    @property
    def order_btn(self):
        return self.find_ele(by=By.CLASS_NAME, value="order_confirm")


    """
        【 页 面 功 能 】
    """

    # 选择不同的下拉框
    def element_action(self):
        self.select_action(self.select_ele, "1")
        self.select_action(self.select_ele, "2")
        self.select_action(self.select_ele, "3")
        self.select_action(self.select_ele, "4")

    # 鼠标悬停
    def mouse_hover(self):
        self.move_to_ele(ele=self.hover_ele)
        time.sleep(3)

    # 鼠标双击
    def mouse_double_click(self):
        self.double_click(ele=self.double_click_ele)
        time.sleep(3)

    # 鼠标拖拽
    def mouse_drag_and_drop(self):
        self.drag_and_drop(s_ele=self.move_source_ele, t_ele=self.move_target_ele)
        time.sleep(3)

    # 键盘 连续按 Tab 键
    def keyboard_tab(self):
        for i in range(3):
            self.keyboard_action(key_action=Keys.TAB)
            time.sleep(2)

    # 点击 alert 弹框 中的确定
    def prompt_alert_confirm(self):
        self.alert_ele.click()
        self.action_alert("accept")

    # 点击 下单 按钮，等待5秒后alert弹框出现，捕获其中的内容
    def click_order_btn(self):
        self.order_btn.click()
        self.condition_wait(condition=expected_conditions.alert_is_present(), timeout=6)
        alter = self.driver.switch_to.alert
        order_id = alter.text
        alter.accept()
        return order_id




