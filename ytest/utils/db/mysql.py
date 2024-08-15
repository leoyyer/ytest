#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :mysql.py
@说明        :
@时间        :2023/05/08 15:07:04
@作者        :Leo
@版本        :1.0
"""
import sys
import os
import pymysql

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
from ytest.common.control.exc import SQLExecuteError
from ytest.common.conf.conf import Config


class MysqlDb:

    def __init__(self, database, project, env=None, time_out=30):
        # 通过字典拆包传递配置信息，建立数据库连接
        self.conf = Config(project, env)
        DB_CONF = {
            "host": self.conf.get_conf("mysql", "mysql_host"),
            "port": int(self.conf.get_conf("mysql", "mysql_port")),
            "user": self.conf.get_conf("mysql", "mysql_user"),
            "password": self.conf.get_conf("mysql", "mysql_passwd"),
        }
        DB_CONF["db"] = database
        db_conf = DB_CONF
        try:
            self.conn = pymysql.connect(
                **db_conf, autocommit=True, connect_timeout=time_out
            )
            # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            raise SQLExecuteError(f"Mysql出现错误，错误原因: {e}")

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def release(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        result = self.cur.fetchall()
        return result

    def execute_db(self, sql):
        """更新/新增/删除"""
        # try:
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 提交事务
        self.conn.commit()
        # except Exception as e:
        #     logger.info("操作MySQL出现错误，错误原因：{}".format(e))
        #     # 回滚所有更改
        #     self.conn.rollback()


# TODO: 使用单例实现
# db = MysqlDb(DB_CONF)

if __name__ == "__main__":
    DB = MysqlDb("db_demo", "demo")
    result = DB.select_db("select id from product_app limit 2;")
