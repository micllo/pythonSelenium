# -*- coding:utf-8 -*-
from Base.base import Base
from selenium.webdriver.common.by import By
import time


class BaiduPage(Base):

    # '搜索'输入框
    def search_field(self):
        return self.find_ele(By.ID, "kw")

    def search_btn(self):
        return self.find_ele(By.ID, "su")

    def search_func(self, content):
        self.search_field().clear()
        self.search_field().send_keys(content)
        time.sleep(2)
        self.search_btn().click()
        time.sleep(2)
        return self.url()
