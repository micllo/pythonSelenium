# -*- coding:utf-8 -*-
from Base.browser_action import Base
from selenium.webdriver.common.by import By
import time


class SearchPage(Base):

    """
        【 元 素 定 位 】
    """

    # '出发城市'输入框
    def search_leave(self):
        return self.find_ele(By.ID, "notice01")

    # '到达城市'输入框
    def search_arrive(self):
        return self.find_ele(By.ID, "notice08")

    # '出发时间'控件
    def search_date(self):
        return self.find_ele(By.ID, "dateObj")

    # '单程'tab控件
    def search_current(self):
        return self.find_ele(By.CSS_SELECTOR, "#searchtype > li.current")

    # '开始搜索'按钮
    def search_btn(self):
        return self.find_ele(By.ID, "searchbtn")

    # 通过js为'出发时间'控件赋值
    def search_js(self, value):
        js_value = "document.getElementById('dateObj').value='%s'" % (value)
        self.js(js_value)

    """
        【 页 面 功 能 】
    """

    def search_train(self, leave, arrive, leave_date, case_instance):

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="train_search_1.png", case_instance=case_instance,
                                           content="首页", time_out=20, error_msg="页面跳转失败！- 找不到'首页'内容")

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
        self.search_js(leave_date)

        # 点击'单程'tab
        self.search_current().click()

        # 单击'开始搜索'按钮
        self.screenshot("train_search_2.png", case_instance)
        self.search_btn().click()
        time.sleep(4)

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="train_search_3.png", case_instance=case_instance,
                                           content="高级软卧", time_out=20, error_msg="页面跳转失败！- 找不到'高级软卧'内容")







