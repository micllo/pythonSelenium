# -*- coding:utf-8 -*-
import unittest
from Base.browser_action import get_driver_func
from Common.com_func import log
from Config import global_var as gv
from Tools.mongodb import MongodbUtils
from Config import config as cfg
from Common.test_func import mongo_exception_send_DD


class ParaCase(unittest.TestCase):

    def __init__(self, test_method="test_", browser_name="Chrome", remote=False, driver=None):
        """
        :param test_method:
        :param browser_name:
        :param remote:
        :param driver:
         【 注意：'test_method'这个参数必须是测试类中存在的以'test_'开头的方法 】
        """
        super(ParaCase, self).__init__(test_method)
        self.driver = driver
        self.log = log
        self.test_method = test_method
        self.browser_name = browser_name
        self.remote = remote

    def setUp(self):
        driver_func = get_driver_func(browser_name=self.browser_name, remote=self.remote)
        self.driver = driver_func()
        self.driver.implicitly_wait(gv.IMPLICITY_WAIT)
        self.driver.set_page_load_timeout(gv.PAGE_LOAD_TIME)  # 页面加载超时
        # 截图ID列表
        self.screen_shot_id_list = []
        # 截图ID列表名称
        self.screen_shot_id_list_name = self.__class__.__name__ + "." + self.test_method
        # 获取当前的'类名/方法名/'(提供截屏路径)
        self.class_method_path = self.__class__.__name__ + "/" + self.test_method + "/"
        # self.driver.maximize_window()
        # self.driver.set_window_size(width=2000, height=1300)
        # self.driver.set_script_timeout()  # 页面异步js执行超时

    def tearDown(self):
        self.driver.quit()

    @staticmethod
    def parametrize(pro_name, browser_name="Chrome", remote=False, driver=None):
        """
        将'测试类'列表中的'上线'的'测试方法'添加入 suite 实例对象中
        :param pro_name:
        :param browser_name:
        :param remote:
        :param driver:
        :return:
        【 添 加 步 骤 】
        1.根据'测试类'列表，从mongo中获取'上线'状态的'测试用例'列表
        2.循环获取'测试类'列表中的所有'测试方法名称'
        3.将这些'测试方法名称'与mongo中'上线'的'测试方法名称'作比较
        4.匹配成功的，则实例化'测试类'时，并添加入'suite'实例对象中
        【 备 注 】
          实例化'测试类'时，必须带上该类中存在的以'test_'开头的方法名
        """
        from Config.pro_config import get_test_class_list_by_pro_name
        test_class_list = get_test_class_list_by_pro_name(pro_name)
        on_line_test_case = []
        for test_class in test_class_list:
            with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as monitor_db:
                try:
                    query_dict = {"test_class_name": test_class.__name__, "status": True}
                    results = monitor_db.find(query_dict, {"_id": 0})
                    for result in results:
                        on_line_test_case.append(result.get("test_method_name"))
                except Exception as e:
                    mongo_exception_send_DD(e=e, msg="获取'" + pro_name + "'项目测试用例数据")
                    return "mongo error"

        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for test_class in test_class_list:
            test_methods_name = test_loader.getTestCaseNames(test_class)
            for test_method_name in test_methods_name:
                if test_method_name in on_line_test_case:  # 匹配'测试方法'名称
                    test_instance = test_class(test_method=test_method_name, browser_name=browser_name,
                                               remote=remote, driver=driver)
                    suite.addTest(test_instance)
        return suite

