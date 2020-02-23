# -*- coding:utf-8 -*-
from Base.base import Base
from selenium.webdriver.common.by import By
import time


class BookPage(Base):

    # G104车次的 '预订'按钮
    def booking_btn_for_g104(self):
        return self.find_ele(By.XPATH, "//*[starts-with(@id,'tbody-01-G1040')]/div[1]/div[6]/div[1]/a")

    def booking(self):
        try:
            time.sleep(2)
            self.booking_btn_for_g104().click()
            time.sleep(2)
        except:
            self.log.error("车次查询失败！")
        return self.url()