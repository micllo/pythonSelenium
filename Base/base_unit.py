# -*- coding:utf-8 -*-
import unittest
import time
from Common import global_var as gl
from Base.base import get_driver_func
from Common.function import log


class ParaCase(unittest.TestCase):

    """
    注意：'test_method'这个参数必须是测试类中存在的以'test_'开头的方法
    """
    def __init__(self, test_method="test_", driver=None):
        super(ParaCase, self).__init__(test_method)
        self.driver = driver
        self.log = log

    def setUp(self):
        driver_func = get_driver_func(browser_name=gl.BROWSER_NAME, remote=gl.USE_REMOTE)
        self.driver = driver_func()
        self.driver.implicitly_wait(5)
        # self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    """
    实例化'测试类'时，必须带上该类中存在的以'test_'开头的方法名
    '测试类'中有多少'test_'开头的方法，就实例化多少对象
    将所有实例化的对象添加入 suite 对象中
    """
    @staticmethod
    def parametrize(test_class_list, driver=None):
        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for test_class in test_class_list:
            test_methods_name = test_loader.getTestCaseNames(test_class)
            for test_method_name in test_methods_name:
                suite.addTest(test_class(test_method_name, driver=driver))
        return suite
