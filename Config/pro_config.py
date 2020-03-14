from Project.pro_demo_1.test_case.demo_test import DemoTest
from Project.pro_demo_1.test_case.train_test import TrainTest


def get_test_class_list_by_pro_name(pro_name):
    """
    通过'项目名'获取'测试类'列表
    :param pro_name:
    :return:
    """
    if pro_name == "pro_demo_1":
        test_class_list = [DemoTest, TrainTest]
    else:
        test_class_list = None
    return test_class_list

