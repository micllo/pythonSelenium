# -*- coding:utf-8 -*-

# 邮箱配置参数
ERROR_MAIL_HOST = "smtp.163.com"
ERROR_MAIL_ACCOUNT = "miclloo@163.com"
ERROR_MAIL_PASSWD = "qweasd123"  # 客户端授权密码，非登录密码

# 日志、报告、截图 等路径
LOGS_PATH = "/Users/micllo/Documents/works/GitHub/pythonSelenium/Logs/"
REPORTS_PATH = "/Users/micllo/Documents/works/GitHub/pythonSelenium/Reports/"
SCREENSHOTS_PATH = "/Users/micllo/Documents/works/GitHub/pythonSelenium/Screenshots/"

# 构建的时候使用前端静态文件路径 ( Api/__init__.py文件的同级目录 )
GULP_STATIC_PATH = 'static'
GULP_TEMPLATE_PATH = 'templates'

# 服务器地址
SERVER_IP = "127.0.0.1"

# 测试报告地址
TEST_REPORT_URL = "http://" + SERVER_IP + ":8070/test_report_local/report.html"

# nginx中的接口方向代理名称
NGINX_API_PROXY = "api_local"

# 接口地址( uwsgi )
API_ADDR = SERVER_IP + ":8070/" + NGINX_API_PROXY

# Selenium Grid Console
# GRID_REMOTE_ADDR = "10.211.55.6:4444"  # win10虚拟机
GRID_REMOTE_ADDR = SERVER_IP + ":5555"  # docker

# mongo 数据库
MONGODB_ADDR = SERVER_IP + ":27017"
MONGODB_DATABASE = "web_auto_test"

# 报错邮箱地址
MAIL_LIST = ["micllo@126.com"]

# 钉钉通知群
DD_MONITOR_GROUP = "3a2069108f0775762cbbfea363984c9bf59fce5967ada82c78c9fb8df354a624"
DD_AT_PHONES = "13816439135,18717854213"
DD_AT_FXC = "13816439135"

