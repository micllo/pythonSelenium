import os, configparser
import threading


# 获取项目路径
def project_path():
    return os.path.split(os.path.realpath(__file__))[0].split('C')[0]


# 获取'config.ini'文件中的 [testUrl] > url 值
def config_url(test_url):
    config = configparser.ConfigParser()
    config.read(project_path() + "config.ini")
    return config.get(test_url, "url")


# 多线程重载 run 方法
class MyThread(threading.Thread):

    def __init__(self, func, driver, test_class_list):
        super(MyThread, self).__init__()
        # threading.Thread.__init__(self)
        self.func = func
        self.driver = driver
        self.test_class_list = test_class_list

    def run(self):
        print("Starting " + self.name)
        print("Exiting " + self.name)
        self.func(self.driver, self.test_class_list)


if __name__ == "__main__":
    print("项目路径：" + project_path())
    print("被测系统URL：" + config_url("ctrip_url"))
    print()
    print(os.path.split(os.path.realpath(__file__)))
    print(os.path.split(os.path.realpath(__file__))[0])
    print(os.path.split(os.path.realpath(__file__))[0].split('C'))
    print(os.path.split(os.path.realpath(__file__))[0].split('C')[0])


