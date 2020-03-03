# -*-coding: utf-8 -*-

import traceback
from pymongo import MongoClient
from pymongo import ReadPreference
from pymongo.write_concern import WriteConcern
from Config import config as cfg
from gridfs import GridFS
from bson.objectid import ObjectId
from Common.com_func import log, send_DD
import base64

db_pool = {}


class MongodbUtils(object):
    """
    此类用于链接mongodb数据库
    write_concern='majority'：表示所有节点写入成功后，才算成功
    write_concern=2： 表示只需要两个节点写入成功后，即为成功
    """
    def __init__(self, collection="", ip="", port=None, database="",
                 replica_set_name="", read_preference=ReadPreference.SECONDARY_PREFERRED,
                 write_concern="majority"):

        self.collection = collection
        self.ip = ip
        self.port = port
        self.database = database
        self.replica_set_name = replica_set_name
        self.read_preference = read_preference
        self.write_concern = write_concern

        if (ip, port) not in db_pool:
            db_pool[(ip, port)] = self.db_connection()
        elif not db_pool[(ip, port)]:
            db_pool[(ip, port)] = self.db_connection()

        self.db = db_pool[(ip, port)]
        self.db_table = self.db_table_connect()

    def __enter__(self):
        return self.db_table

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def db_connection(self):
        db = None
        try:
            if self.replica_set_name:
                # 当pymongo更新到3.x版本, 连接副本集的方法得用MongoClient, 如果版本<=2.8.1的, 得用MongoReplicaSetClient
                db = MongoClient(self.ip, replicaset=self.replica_set_name)
            else:
                db = MongoClient(self.ip, self.port)
            log.info("mongodb connection success")

        except Exception as e:
            log.error("mongodb connection failed: %s" % self.collection)
            print(e)
            print(traceback.format_exc())
        return db

    def db_table_connect(self):
        db = self.db.get_database(self.database, read_preference=self.read_preference,
                                  write_concern=WriteConcern(w=self.write_concern))
        table_db = db[self.collection]
        return table_db


class MongoGridFS(object):
    """
     备注：
       （1）保存在mongo的'image'数据库中，没有会自动创建
       （2）创建成功后，会在集合中生成'fs.flies'和'fs.chunks'
    """

    def __init__(self):
        self.client = MongoClient("mongodb://" + cfg.MONGODB_IP_PORT)
        self.img_db = self.client["image"]

    def find_exception_send_DD(self, e, msg):
        """
        发现异常时钉钉通知
        :param e:
        :param msg:
        :return:
        """
        title = "[监控]'mongo'存取图片错误通知"
        text = "#### UI自动化测试'mongo'存取图片错误\n\n****操作方式：" + msg + "****\n\n****错误原因：" + str(e) + "****"
        send_DD(dd_group_id=cfg.DD_MONITOR_GROUP, title=title, text=text, at_phones=cfg.DD_AT_FXC, is_at_all=False)

    def upload_file(self, img_file_full):
        """
        上传图片
        :param img_file_full:
        :return:
            1.上传成功 -> 返回 图片id
            2.mongo连接不上 -> 返回 None
        """
        img_file = img_file_full.split("/")[-1]
        img_name = img_file.split(".")[0]
        img_tpye = img_file.split(".")[1]
        gridfs_col = GridFS(self.img_db)
        files_id = None
        try:
            with open(img_file_full, 'rb') as file_r:
                files_id = gridfs_col.put(data=file_r, content_type=img_tpye, filename=img_name)  # 上传到gridfs
        except Exception as e:
            self.find_exception_send_DD(e=e, msg="上传图片")
        finally:
            return files_id

    def get_binary_by_id(self, files_id):
        """
        按文件'files_id'获取图片'二进制文件'
        :param files_id:
        :return:
            1.获取成功 -> 返回 图片二进制文件
            2.找不到该文件 -> 返回 no such file
            3.mongo连接不上 -> 返回 None
        """
        gridfs_col = GridFS(self.img_db)
        img_binary = None
        try:
            gf = gridfs_col.get(file_id=ObjectId(files_id))
            img_binary = gf.read()
        except Exception as e:
            self.find_exception_send_DD(e=e, msg="获取二进制图片")
            if "Connection refused" not in str(e):
                img_binary = "no such file"
        finally:
            log.info("img_binary : " + str(img_binary))
            return img_binary

    def download_file_by_name(self, file_name, out_name):
        """
        按文件名获取图片，保存到'out_name'中
        :param file_name:
        :param out_name:
        :return:
        """
        gridfs_col = GridFS(self.img_db)
        try:
            img_binary = gridfs_col.get_version(filename=file_name, version=1).read()
            with open(out_name, 'wb') as file_w:
                file_w.write(img_binary)
        except Exception as e:
            self.find_exception_send_DD(e=e, msg="获取图片")


if __name__ == '__main__':

    # with MongodbUtils(ip=cfg.MONGODB_IP_PORT, database="monitorAPI", collection="monitorResult") as monitor_db:
    #     res = monitor_db.find_one({"testCaseName": "获取图片验证码_200_MONITOR"}, {"_id": 0})
    #     print(res)
    #     print(monitor_db)

    img_file_full = cfg.SCREENSHOTS_PATH + "TrainTest/test_ctrip/search_train_1.png"
    mgf = MongoGridFS()
    # mgf.upload_file(img_file_full)
    # mgf.get_binary_by_id("5e5cac9188121299450740b3")
    # mgf.download_file_by_name("search_train_3", "/Users/micllo/Downloads/test2.png")




