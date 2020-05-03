# -*- coding:utf-8 -*-
import os, sys
# 将项目根路径添加入path
# sys.path.append(os.path.split(os.getcwd())[0])
import time
from Common.com_func import get_config_ini, log
from TestBase.test_case_unit import ParaCase
from TestBase.browser_action import Base


class DemoTest(ParaCase):

    """ Demo 用 例 集 """

    def test_demo_01(self):
        """ demo 测 试 用 例 test_demo_01  """
        log.info("user(test_demo_01): " + self.user)
        log.info("passwd(test_demo_01): " + self.passwd)

        self.driver.get(get_config_ini("test_url", "baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_demo_01")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('1', "1", "test_demo_01用例测试失败")

    def test_demo_02(self):
        """ demo 测 试 用 例 test_demo_02  """
        log.info("user(test_demo_02): " + self.user)
        log.info("passwd(test_demo_02): " + self.passwd)

        self.driver.get(get_config_ini("test_url", "baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_demo_02")
        self.driver.find_element_by_id("su").click()
        Base.screenshot(self, "test_demo_02.png", self)  # 类调用实例方法
        time.sleep(2)
        self.assertIn('test_demo_01', "2", "test_demo_02用例测试失败")


