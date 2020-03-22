# -*- coding:utf-8 -*-

# 邮箱配置参数
ERROR_MAIL_HOST = "smtp.163.com"
ERROR_MAIL_ACCOUNT = "miclloo@163.com"
ERROR_MAIL_PASSWD = "qweasd123"  # 客户端授权密码，非登录密码

# 日志、报告、截图 等路径
LOGS_PATH = "/opt/project/logs/"
REPORTS_PATH = "/opt/project/reports/"
SCREENSHOTS_PATH = "/opt/project/screenshots/"

# 构建的时候使用前端静态文件路径 ( Api/__init__.py文件的同级目录 )
GULP_STATIC_PATH = '../Build'
GULP_TEMPLATE_PATH = '../Build/templates'

# 服务器地址
# SERVER_IP_PORT = "192.168.3.102"  #  MERCURY_1602
SERVER_IP = "192.168.31.10"  # Demba Ba_5G

# 是否启用远程浏览器
REMOTE = True

# 测试报告地址
BASE_REPORT_PATH = "http://" + SERVER_IP + ":1080/test_report/"
CURRENT_REPORT_URL = BASE_REPORT_PATH + "report.html"
HISTORY_REPORT_PATH = BASE_REPORT_PATH + "history/"

# nginx中的接口方向代理名称
NGINX_API_PROXY = "api"

# 接口地址
API_ADDR = SERVER_IP + ":1080/" + NGINX_API_PROXY

# Selenium Grid Console
# GRID_REMOTE_ADDR = "10.211.55.6:4444"  # win10虚拟机
GRID_REMOTE_ADDR = SERVER_IP + ":5555"  # docker

# mongo 数据库
MONGODB_ADDR = SERVER_IP + ":27027"
MONGODB_DATABASE = "web_auto_test"

# 报错邮箱地址
MAIL_LIST = ["micllo@126.com"]

# 钉钉通知群
DD_MONITOR_GROUP = "3a2069108f0775762cbbfea363984c9bf59fce5967ada82c78c9fb8df354a624"
DD_AT_PHONES = "13816439135,18717854213"
DD_AT_FXC = "13816439135"

