# -*- coding: utf-8 -*-
from api import flask_app


@flask_app.route("/")
def server_index():
    server_info = "UI自动化测试版本：V1.0.00R200213"
    return server_info


if __name__ == '__main__':
    flask_app.run(host="0.0.0.0", port=7788, debug=True)