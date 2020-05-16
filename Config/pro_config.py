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


def pro_exist(pro_name):
    """
    判断项目名称是否存在
    :param pro_name:
    :return:
    """
    pro_name_list = ["pro_demo_1", "pro_demo_2"]
    if pro_name in pro_name_list:
        return True
    else:
        return False


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

