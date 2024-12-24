#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :Mysql.py
@说明        :
@时间        :2024/12/23 16:25:26
@作者        :Leo
@版本        :1.0
"""

import pymysql
from ytest.config.ConfFile import ConfigFile
from pymysql.cursors import DictCursor


# 定义单例装饰器
def singleton(cls):
    """
    单例装饰器，确保每个类只有一个实例。

    Args:
        cls: 需要转换为单例的类。

    Returns:
        一个确保只有一个实例的装饰器函数。
    """
    instances = {}  # 用于存储类实例的字典

    def get_instance(*args, **kwargs):
        """
        获取类实例，如果实例已创建，则返回已创建的实例。

        Args:
            *args: 类构造函数的非关键字参数。
            **kwargs: 类构造函数的关键字参数。

        Returns:
            cls: 类的单例实例。
        """
        if cls not in instances:
            # 如果类的实例不存在，则创建并保存实例
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton  # 使用装饰器将 MysqlDb 转化为单例模式
class MysqlDb:
    """
    这是一个用于连接和操作 MySQL 数据库的类。
    使用单例模式，确保每次使用的都是同一个实例。
    """

    def __init__(self, database, project, env=None, time_out=30):
        """
        初始化 MySQL 数据库连接。

        Args:
            database: 要连接的数据库名称。
            project: 项目名称，用于从配置文件中获取配置信息。
            env: 环境，默认为 None。
            time_out: 连接超时设置，默认为 30 秒。
        """
        # 加载配置文件
        self.conf = ConfigFile(project, env)
        DB_CONF = {
            "host": self.conf.get_conf("mysql", "mysql_host"),
            "port": int(self.conf.get_conf("mysql", "mysql_port")),
            "user": self.conf.get_conf("mysql", "mysql_user"),
            "password": self.conf.get_conf("mysql", "mysql_passwd"),
        }
        DB_CONF["db"] = database
        db_conf = DB_CONF
        try:
            # 创建数据库连接
            self.conn = pymysql.connect(
                **db_conf, autocommit=True, connect_timeout=time_out
            )
            # 创建游标对象，结果以字典格式返回
            self.cur = self.conn.cursor(cursor=DictCursor)
        except Exception as e:
            raise pymysql.MySQLError(f"Mysql出现错误，错误原因: {e}")

    def __del__(self):
        """
        在对象被销毁时关闭游标和连接。
        """
        self.release()

    def release(self):
        """
        关闭游标和数据库连接。
        """
        if hasattr(self, "cur"):
            self.cur.close()
        if hasattr(self, "conn"):
            self.conn.close()

    def select_db(self, sql):
        """
        查询操作，执行 SELECT SQL 查询并返回结果。

        Args:
            sql: 执行的 SQL 查询语句。

        Returns:
            查询结果（以字典形式返回）。
        """
        self.conn.ping(reconnect=True)  # 检查数据库连接是否断开，自动重连
        self.cur.execute(sql)  # 执行 SQL
        return self.cur.fetchall()  # 返回查询结果

    def execute_db(self, sql):
        """
        执行更新、插入或删除操作。

        Args:
            sql: 执行的 SQL 语句（INSERT/UPDATE/DELETE）。
        """
        self.conn.ping(reconnect=True)  # 检查数据库连接是否断开，自动重连
        self.cur.execute(sql)  # 执行 SQL
        self.conn.commit()  # 提交事务


if __name__ == "__main__":
    DB1 = MysqlDb("db_demo", "demo")
    DB2 = MysqlDb("test_db", "demo_project")
    result = DB1.select_db("select id from product_app limit 2;")
