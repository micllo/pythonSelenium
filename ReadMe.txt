
【 本地 Mac 相关 】

1.uWSGI配置文件：./vassals/mac_app_uwsgi.ini

2.启动 uWSGI 命令 在 ./start_uwsgi_local.sh 脚本

3.停止 uWSGI 命令 在 ./stop_uwsgi.sh 脚本

3.本地的 Logs、Reports、Screenshot、vassals_local、venv 三个目录上传 GitHub 时被忽略

4.本地部署步骤：
（1）将本地代码拷贝入临时文件夹，并删除不需要的文件目录：Logs、Reports、Screenshot、vassals_local、venv
（2）将零时文件夹中的该项目压缩打包，上传至服务器的临时文件夹中
（3）在服务器中进行部署操作：停止nginx、mongo、uwsgi服务 -> 替换项目、uwsgi.ini配置文件 -> 替换config配置文件 -> 启动nginx、mongo、uwsgi服务
（4）删除本地的临时文件夹

5.访问地址（ server.py 启动 ）：
（1）接口地址 -> http://127.0.0.1:8082/
               http://127.0.0.1:8082/UI/sync_run_case
               http://127.0.0.1:8082/UI/get_img/5e5cac9188121299450740b3

6.访问地址（ uwsgi 启动 ）：
（1）测试报告 -> http://127.0.0.1:8070/test_report_local/report.html
（2）接口地址 -> http://127.0.0.1:8070/api_local/
               http://127.0.0.1:8070/api_local/UI/sync_run_case
               http://127.0.0.1:8070/api_local/UI/get_img/5e5cac9188121299450740b3

   （ 备注：uwgsi 启动 8081 端口、nginx 配置 8070 反向代理 8081 ）


##################################################################################3


【 Docker centos7 相关 】

1.uWSGI配置文件：vassals_docker/app_uwsgi.ini

2.启动 uWSGI 命令 在 ./start_uwsgi.sh 脚本

3.停止 uWSGI 命令 在 ./stop_uwsgi.sh 脚本

4.部署时的存放位置：
（1）./pythonSelenium -> /opt/project/pythonSelenium
（2）./pythonSelenium/vassals/app_uwsgi.ini -> /etc/uwsgi/vassals/app_uwsgi.ini

5.部署时相关配置文件的替换操作：
（1）将./Config/目录下的 config.py 删除
（2）将./Config/目录下的 config_docker.py 重命名为 config.py

6.目录结构
  /var/log/uwsgi/ 		   -> pid_uwsgi.pid、app_uwsgi.log、emperor.log
  /var/log/nginx/ 		   -> error.log、access.log
  /etc/uwsgi/vassals/	   -> app_uwsgi.ini
  /opt/project/logs/ 	   -> 项目日志
  /opt/project/reports/	   -> 测试报告
  /opt/project/${pro_name} -> 项目
  /opt/project/tmp         -> 临时目录(部署时使用)


7.服务器部署命令：
（1）从GitGub上拉取代码至临时目录
（2）关闭nginx、mongo、uwsgi服务
（3）替换项目、uwsgi.ini配置文件
（4）替换config配置文件：删除'config.py'、将'config.py'重命名为'config.py'
（5）启动nginx、mongo、uwsgi服务
（6）清空临时文件


8.访问地址（ Docker 内部 ）：
（1）测试报告 -> http://127.0.0.1:80/test_report/report.html
（2）接口地址 -> http://127.0.0.1:80/api/
               http://127.0.0.1:80/api/UI/sync_run_case
    ( 备注：uwgsi 启动 8081 端口、nginx 配置 80 反向代理 8081 )

9.访问地址（ 外部访问 ）：
（1）测试报告 -> http://192.168.31.10:1080/test_report/report.html
（2）接口地址 -> http://192.168.31.10:1080/api/
               http://192.168.31.10:1080/api/UI/sync_run_case
               http://192.168.31.10:1080/api/UI/get_img/5e5cac9188121299450740b3
    ( 备注：docker 配置 1080 映射 80 )


10.关于部署
（1）方式一：通过'fabric'工具进行部署 -> ./Deploy/local_deploy.py
（2）方式二：通过'shell'脚本命令进行部署
            sh /Users/micllo/Documents/works/expect-deploy/docker_python/deploy.sh pythonSelenium 127.0.0.1 1022


11.关于 Selenium Grid Console
（1）Hub 界面地址
    http://localhost:5555/grid/console
    http://192.168.31.10:5555/grid/console
（2）使用mac自带的远程桌面工具进入debug模式的界面
    在Finder图标右键选择'连接服务器' -> vnc://127.0.0.1:5911 -> 默认密码：secret