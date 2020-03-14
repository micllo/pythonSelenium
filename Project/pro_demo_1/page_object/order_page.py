# -*- coding:utf-8 -*-
from Base.browser_action import Base
from selenium.webdriver.common.by import By
import time


class OrderPage(Base):

    """
        【 元 素 定 位 】
    """

    # '姓名'输入框
    def name_field(self):
        return self.find_ele(By.CSS_SELECTOR, "#pasglistdiv > div > ul > li:nth-child(2) > input")

    """
        【 页 面 功 能 】
    """

    def user_info(self, name):
        self.name_field().send_keys(name)
        time.sleep(3)
        return self.url()
