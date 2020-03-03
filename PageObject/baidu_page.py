# -*- coding:utf-8 -*-
from Base.browser_action import Base
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

    def search_func(self, content, case_instance):
        self.search_field().clear()
        self.search_field().send_keys(content)
        time.sleep(2)
        self.screenshot("test_baidu_1.png", case_instance)
        self.search_btn().click()
        time.sleep(2)
        return self.url()
