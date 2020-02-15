import os, sys
# 将项目根路径添加入path
sys.path.append(os.path.split(os.getcwd())[0])
import unittest, time
from Common.function import config_url, project_path
from Common.excel_data import read_excel
from HTMLTestRunnerCN import HTMLTestRunner
from selenium import webdriver
from PageObject.book_page import BookPage
from PageObject.order_page import OrderPage
from PageObject.search_page import SearchPage
from PageObject.baidu_page import BaiduPage
from Base.base_unit import ParaCase


class TrainTest(ParaCase):

    """ 携 程 订 票 用 例 集"""

    # 所有case运行前只运行一次
    @classmethod
    def setUpClass(cls):
        cls.data = read_excel(project_path() + "Data/testdata.xlsx", 0)
        # cls.driver = webdriver.Chrome()
        # cls.driver.implicitly_wait(10)
        # cls.driver.get(config_url())
        # # cls.driver.maximize_window()

    # 所有case运行后只运行一次
    @classmethod
    def tearDownClass(cls):
        pass

    def test_01(self):
        """ 携 程 订 票 测 试 用 例 test_01  """
        self.driver.get(config_url("baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_01")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('1', "3")

    def test_02(self):
        """ 携 程 订 票 测 试 用 例 test_02  """
        self.driver.get(config_url("baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_01")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('1', "2")

    def test_ctrip(self):
        """ 携 程 订 票 测 试 用 例 test_ctrip  """
        self.driver.get(config_url("ctrip_url"))
        search_page = SearchPage(self.driver)
        res_url = search_page.search_train(self.data.get(1)[0], self.data.get(1)[1], self.data.get(1)[2])
        # print(res_url)
        # 断言：返回的url中是否包含'TrainBooking'
        time.sleep(3)
        self.assertIn('TrainBooking', res_url)

    def test_baidu(self):
        """ 携 程 订 票 测 试 用 例 test_baidu  """
        self.driver.get(config_url("baidu_url"))
        search_page = BaiduPage(self.driver)
        res_url = search_page.search_func("selenium")
        time.sleep(2)
        self.assertIn("wd=selenium", res_url)



    # def test_02(self):
    #     book = BookPage(self.driver)
    #     res = book.booking()
    #     self.assertIn("InputPassengers", res)
    #
    # def test_o3(self):
    #     order = OrderPage(self.driver)
    #     res = order.user_info("测试人员")
    #     self.assertIn("RealTimePay", res)

