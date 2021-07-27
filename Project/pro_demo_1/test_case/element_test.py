# -*- coding:utf-8 -*-
import time
from Common.com_func import log, project_path
from TestBase.test_case_unit import ParaCase
from Project.pro_demo_1.page_object.element_page import ElementPage


class ElementTest(ParaCase):

    """ 元 素 定 位 用 例 集 """

    def test_element_01(self):
        """ 元素定位用例01  """
        log.info("user(test_demo_01): " + self.user)
        log.info("passwd(test_demo_01): " + self.passwd)

        self.driver.get("file://" + project_path() + "Api/templates/element_demo.html")
        time.sleep(2)
        ele_page = ElementPage(self)
        ele_page.element_action()
        # ele_page.mouse_hover()
        # ele_page.mouse_double_click()
        # ele_page.mouse_drag_and_drop()
        # ele_page.prompt_alert_confirm()
        # ele_page.keyboard_tab()
        order_id = ele_page.click_order_btn()
        time.sleep(2)
        self.assertIn(order_id, "20180101151010", "test_element_01用例测试失败")


