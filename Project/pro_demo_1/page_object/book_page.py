# -*- coding:utf-8 -*-
from Base.browser_action import Base
from selenium.webdriver.common.by import By
import time


class BookPage(Base):

    """
        【 元 素 定 位 】
    """

    # G104车次的 '预订'按钮
    def booking_btn_for_g104(self):
        return self.find_ele(By.XPATH, "//*[starts-with(@id,'tbody-01-G1040')]/div[1]/div[6]/div[1]/a")

    """
        【 页 面 功 能 】
    """

    def booking(self):
        try:
            time.sleep(2)
            self.booking_btn_for_g104().click()
            time.sleep(2)
        except:
            self.log.error("车次查询失败！")
        return self.url()