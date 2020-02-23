#!/bin/bash

# 批量 执行命令 emperor：
# 1.批量启动 vassals 目录下的 uwsgi 项目
# 2.监视 vassals 目录下的 ini 配置文件
# --uid centos ：让 centos 用户 有权限管理
# --gid centos ：让 centos 组 有权限管理
nohup /usr/bin/uwsgi --master --emperor /etc/uwsgi/vassals --die-on-term --uid centos --gid centos --logto /var/log/uwsgi/emperor.log > /dev/null 2>&1 &
