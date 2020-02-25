# -*- coding: utf-8 -*-
from fabric.api import *
from Common.function import mkdir
import time


# 设置变量
host = "127.0.0.1"
port = "1022"
user = "centos"
passwd = "centos"
pro_name = "pythonSelenium"
pro_name_tar = pro_name + ".tar.gz"
tmp_path = "/Users/micllo/tmp/"
pro_tmp_path = tmp_path + pro_name
deploy_file = tmp_path + pro_name_tar
pro_path = "/Users/micllo/Documents/works/GitHub/" + pro_name
remote_tmp_path = "/opt/project/tmp/"


# 本地操作
def local_action():
    # 若临时目录不存在则创建
    mkdir(tmp_path)
    # 清空临时目录中的内容, 将项目代码拷贝入临时文件夹
    with lcd(tmp_path):
        local("rm -rf " + pro_name)
        local("rm -rf " + deploy_file)
        local("cp -r " + pro_path + " " + tmp_path)
    # 删除临时文件夹中不需要的文件目录
    with lcd(pro_tmp_path):
        local("rm -rf .DS_Store")
        local("rm -rf .git")
        local("rm -rf .gitignore")
        local("rm -rf .idea")
        local("rm -rf Logs")
        local("rm -rf Reports")
        local("rm -rf Screenshots")
        local("rm -rf vassals_local")
        local("rm -rf venv")
        local("rm -rf Deploy")
        local("ls")
    # 归档压缩 临时文件夹中的项目（ 可以不进入目录，直接执行 ）
    with lcd(tmp_path):
        local("tar -czvf " + pro_name_tar + " " + pro_name)
    # 将部署文件上传服务器
    with settings(host_string="%s@%s:%s" % (user, host, port), password=passwd):
        put(remote_path=remote_tmp_path, local_path=deploy_file)


# 服务器端操作
def server_action():
    with settings(host_string="%s@%s:%s" % (user, host, port), password=passwd):
        # 停止'nginx'和'uwsgi'服务
        run("sh /home/centos/stop_nginx.sh", warn_only=True)  # 忽略失败的命令,继续执行
        run("sh /home/centos/stop_uwsgi.sh", warn_only=True)
        run("pwd")
        # 解压'部署文件'
        run("tar -xzvf " + remote_tmp_path + pro_name_tar + " -C " + remote_tmp_path, warn_only=True)
        # 替换'项目'和'uwsgi.ini'配置文件
        with cd(remote_tmp_path):
            run("rm -rf /opt/project/" + pro_name, warn_only=True)
            run("cp -r " + pro_name + " /opt/project/", warn_only=True)
            run("rm -r /etc/uwsgi/vassals/*.ini", warn_only=True)
            run("cp -r /opt/project/" + pro_name + "/vassals/*.ini /etc/uwsgi/vassals/", warn_only=True)
        # 替换config配置文件
        with cd("/opt/project/" + pro_name + "/Config"):
            run("rm -r config.py && mv config_docker.py config.py", warn_only=True)

        # 启动'nginx'和'uwsgi'服务
        run("sh /home/centos/start_nginx.sh", warn_only=False)  # 不忽略失败的命令，不能继续执行
        run("sh /home/centos/start_uwsgi.sh", warn_only=False, pty=False)  # 参数pty：解决'fabric'执行'nohub'的问题

        # 清空临时文件夹
        with cd(remote_tmp_path):
            run("rm -rf " + pro_name, warn_only=True)
            run("rm -rf " + pro_name + ".tar.gz", warn_only=True)


if __name__ == "__main__":
    local_action()
    server_action()

