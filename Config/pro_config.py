from Project.pro_demo_1.test_case.demo_test import DemoTest
from Project.pro_demo_1.test_case.train_test import TrainTest
from Project.pro_demo_1.test_case.element_test import ElementTest
import os

# 配置 项目名称列表
pro_name_list = ["pro_demo_1", "pro_demo_2"]


def get_test_class_list(pro_name):
    """
    通过'项目名'获取'测试类'列表
    :param pro_name:
    :return:
    """
    if pro_name == "pro_demo_1":
        test_class_list = [DemoTest, TrainTest, ElementTest]
    else:
        test_class_list = None
    return test_class_list


def get_login_accout(thread_name_index):
    """
    通过线程名的索引 获取登录账号
    :param thread_name_index:
    :return:
    """
    if thread_name_index == 1:
        return "user_1", "passwd_1"
    elif thread_name_index == 2:
        return "user_2", "passwd_2"
    elif thread_name_index == 3:
        return "user_3", "passwd_3"
    elif thread_name_index == 4:
        return "user_4", "passwd_4"
    elif thread_name_index == 5:
        return "user_5", "passwd_5"
    else:
        return "user_6", "passwd_6"


if __name__ == "__main__":
    pro_path = os.path.split(os.path.realpath(__file__))[0].split('C')[0]
    print(pro_path)

