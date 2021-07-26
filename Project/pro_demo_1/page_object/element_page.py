# -*- coding:utf-8 -*-
from TestBase.browser_action import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 键盘操作
import time


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
        self.move_to_ele(self.hover_ele)
        time.sleep(3)

    # 鼠标双击
    def mouse_double_click(self):
        self.double_click(self.double_click_ele)
        time.sleep(3)

    # 鼠标拖拽
    def mouse_drag_and_drop(self):
        self.drag_and_drop(self.move_source_ele, self.move_target_ele)
        time.sleep(3)

    # 键盘 连续按 Tab 键
    def keyboard_tab(self):
        self.keyboard_action(Keys.TAB)
        time.sleep(2)
        self.keyboard_action(Keys.TAB)
        time.sleep(2)
        self.keyboard_action(Keys.TAB)
        time.sleep(2)

