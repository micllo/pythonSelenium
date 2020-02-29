# -*- coding:utf-8 -*-
import unittest
from Base.base import get_driver_func
from Common.function import log
from Config import global_var as gv


class ParaCase(unittest.TestCase):

    """
    注意：'test_method'这个参数必须是测试类中存在的以'test_'开头的方法
    """
    def __init__(self, test_method="test_", browser_name="Chrome", remote=False, driver=None):
        super(ParaCase, self).__init__(test_method)
        self.driver = driver
        self.log = log
        self.browser_name = browser_name
        self.remote = remote

    def setUp(self):
        driver_func = get_driver_func(browser_name=self.browser_name, remote=self.remote)
        self.driver = driver_func()
        self.driver.implicitly_wait(gv.IMPLICITY_WAIT)
        self.driver.set_page_load_timeout(gv.PAGE_LOAD_TIME)  # 页面加载超时
        # self.driver.maximize_window()
        # self.driver.set_window_size(width=2000, height=1300)
        # self.driver.set_script_timeout()  # 页面异步js执行超时

    def tearDown(self):
        self.driver.quit()

    """
    实例化'测试类'时，必须带上该类中存在的以'test_'开头的方法名
    '测试类'中有多少'test_'开头的方法，就实例化多少对象
    将所有实例化的对象'test_instance'添加入 suite 对象中
    """
    @staticmethod
    def parametrize(test_class_list, browser_name="Chrome", remote=False, driver=None):
        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for test_class in test_class_list:
            test_methods_name = test_loader.getTestCaseNames(test_class)
            for test_method_name in test_methods_name:
                test_instance = test_class(test_method=test_method_name, browser_name=browser_name,
                                           remote=remote, driver=driver)
                suite.addTest(test_instance)
        return suite
