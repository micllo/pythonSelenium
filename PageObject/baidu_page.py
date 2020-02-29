# -*- coding:utf-8 -*-
from Base.base import Base
from selenium.webdriver.common.by import By
import time


class BaiduPage(Base):

    """
        【 元 素 定 位 】
    """

    # '搜索'输入框
    def search_field(self):
        return self.find_ele(By.ID, "kw")

    def search_btn(self):
        return self.find_ele(By.ID, "su")

    """
        【 页 面 功 能 】
    """

    def search_func(self, content, class_method_path):
        self.search_field().clear()
        self.search_field().send_keys(content)
        time.sleep(2)
        self.screenshot(class_method_path, "test_baidu_1.png")
        self.search_btn().click()
        time.sleep(2)
        return self.url()
