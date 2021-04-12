# -*- coding:utf-8 -*-
from TestBase.browser_action import Base
from selenium.webdriver.common.by import By
import time


class SearchPage(Base):

    """
        【 元 素 定 位 】
    """

    # '出发城市'输入框
    def search_leave(self):
        return self.find_ele(By.ID, "departCityName")

    # '到达城市'输入框
    def search_arrive(self):
        return self.find_ele(By.ID, "arriveCityName")

    # '出发时间'控件
    def search_date(self):
        return self.find_ele(By.ID, "departDate")

    # '单程'tab控件
    def search_current(self):
        # return self.find_ele(By.CSS_SELECTOR, "#search_type > li.current")
        return self.find_ele(By.XPATH, "//*[@id='searchBoxTemplete']/div/div[1]/div[2]/ul/li[1]")

    # '开始搜索'按钮
    def search_btn(self):
        return self.find_ele(By.CLASS_NAME, "searchbtn")

    def get_gepart_date_ele_id(self):
        return "departDate"

    # 通过js为'出发时间'控件赋值
    def search_js(self, ele_id, value):
        # js_value = "document.getElementById('dateObj').value='%s'" % (value)
        js_value = "document.getElementById('" + ele_id + "').value='%s'" % (value)
        self.js(js_value)

    """
        【 页 面 功 能 】
    """

    def search_train(self, leave, arrive, leave_date):

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="train_search_1.png", content="首页", error_msg="页面跳转失败！- 找不到'首页'内容")

        old_handle = self.open_new_window()
        time.sleep(2)
        self.close()
        time.sleep(2)
        self.driver.switch_to.window(old_handle)

        # 输入'出发城市'
        self.search_leave().clear()
        self.search_leave().send_keys(leave)
        time.sleep(2)

        # 输入'到达城市'
        self.search_arrive().clear()
        self.search_arrive().send_keys(arrive)
        time.sleep(2)

        # 输入'出发时间'（ 通过js ）
        self.search_js(self.get_gepart_date_ele_id(), leave_date)
        time.sleep(3)

        # 点击'单程'tab
        self.search_current().click()

        # 单击'开始搜索'按钮
        self.screenshot("train_search_2.png")
        self.search_btn().click()
        time.sleep(4)

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="train_search_3.png", content="高级软卧", error_msg="页面跳转失败！- 找不到'高级软卧'内容")







