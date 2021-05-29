# -*- coding:utf-8 -*-
import os, sys
# 将项目根路径添加入path
sys.path.append(os.path.split(os.getcwd())[0])
import time
from Common.com_func import get_config_ini, project_path, log
from Tools.excel_data import read_excel
from Project.pro_demo_1.page_object.search_page import SearchPage
from Project.pro_demo_1.page_object.baidu_page import BaiduPage
from TestBase.test_case_unit import ParaCase
from TestBase.browser_action import Base


class TrainTest(ParaCase):

    """ 携 程 订 票 用 例 集 """

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
        """ 订票用例01  """
        log.info("user(test_01): " + self.user)
        log.info("passwd(test_01): " + self.passwd)

        self.driver.get(get_config_ini("test_url", "baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_01")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('test_01', "1", "test_01用例测试失败")

    def test_02(self):
        """ 订票用例02  """
        log.info("user(test_02): " + self.user)
        log.info("passwd(test_02): " + self.passwd)

        self.driver.get(get_config_ini("test_url", "baidu_url"))
        self.driver.find_element_by_id("kw8888").send_keys("test_01")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('test_02', "test_02", "test_02用例测试失败")

    # def test_baidu(self):
    #     """ 测 试 用 例 test_baidu  """
    def test_03(self):
        """ 订票用例03 """
        log.info("user(test_baidu): " + self.user)
        log.info("passwd(test_baidu): " + self.passwd)

        self.driver.get(get_config_ini("test_url", "baidu_url"))
        time.sleep(1)

        # 通过Base类调用实例方法 ：self（测试用例实例对象）
        Base.screenshot(self, "test_baidu_1.png")

        baidu_page = BaiduPage(self)
        res_url = baidu_page.search_func("selenium")
        time.sleep(2)
        self.assertIn("wd=selenium", res_url, "test_baidu用例测试失败")

    def test_ctrip(self):
        """ 订票用例04 """
        log.info("user(test_ctrip): " + self.user)
        log.info("passwd(test_ctrip): " + self.passwd)

        # 根据不同用例特定自定义设置（也可以不设置）
        self.driver.set_window_size(width=2000, height=1300)
        self.driver.implicitly_wait(5)

        # 打开测试页面(设置浏览器大小)
        self.driver.get(get_config_ini("test_url", "ctrip_url"))

        # 在搜索页面中 执行查询功能
        search_page = SearchPage(self)
        search_page.search_train(self.data.get(1)[0], self.data.get(1)[1], self.data.get(1)[2])

    def test_page_load(self):
        # """  页面加载用例  """
        """ 订票用例05 """
        log.info("user(test_page_load): " + self.user)
        log.info("passwd(test_page_load): " + self.passwd)

        test_url = "https://www.163.com/"
        Base.get_page_with_time_out(self, test_url, 2)
        self.driver.find_element_by_xpath("//*[@id='app_list']/li[1]/a").click()
        time.sleep(3)
        self.assertTrue(Base.content_is_exist(self, "网易新闻", 5), "test_page_load 页面内容没有找到！")

