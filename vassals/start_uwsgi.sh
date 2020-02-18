#!/bin/bash

# 单个 执行命令
# uwsgi --ini /Users/micllo/Documents/works/GitHub/pythonSelenium/vassals/mac_app_uwsgi.ini

# 批量 执行命令 emperor：
# 1.批量启动 vassals 目录下的 uwsgi 项目
# 2.监视 vassals 目录下的 ini 配置文件
# --uid centos ：让 centos 用户 有权限管理
# --gid centos ：让 centos 组 有权限管理
uwsgi --master --emperor /Users/micllo/Documents/works/GitHub/pythonSelenium/vassals --die-on-term --logto /Users/micllo/Documents/works/GitHub/pythonSelenium/Logs/emperor.log
