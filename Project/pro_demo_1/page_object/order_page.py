# -*- coding:utf-8 -*-
from TestBase.browser_action import Base
from TestBase.webdriver_package import *


class OrderPage(Base):

    """
        【 元 素 定 位 】
    """

    # '姓名'输入框
    def name_field(self):
        return self.find_ele(By.CSS_SELECTOR, "#inputPassengerVue > div.pasg-add > ul > li:nth-child(2) > input")

    """
        【 页 面 功 能 】
    """

    def user_info(self, name):
        self.name_field().send_keys(name)
        time.sleep(3)
        return self.url()
