import os, sys
# 将项目根路径添加入path
sys.path.append(os.path.split(os.getcwd())[0])
import time
from Common.function import get_config_ini, project_path
from Base.base_unit import ParaCase


class DemoTest(ParaCase):

    """ Demo 用 例 集 """

    def test_demo_01(self):
        """ demo 测 试 用 例 test_demo_01  """
        self.driver.get(get_config_ini("test_url", "baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_demo_01")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('1', "1")

    def test_demo_02(self):
        """ demo 测 试 用 例 test_demo_02  """
        self.driver.get(get_config_ini("test_url", "baidu_url"))
        self.driver.find_element_by_id("kw").send_keys("test_demo_02")
        self.driver.find_element_by_id("su").click()
        time.sleep(2)
        self.assertIn('1', "2")

