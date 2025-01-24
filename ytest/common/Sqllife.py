#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :Sqllife.py
@说明        :
@时间        :2024/12/23 16:23:58
@作者        :Leo
@版本        :1.0
"""

from icecream import ic
import sqlite3
from datetime import datetime, timedelta


class YtestDatabase:
    def __init__(self, db_name="ytest.db"):
        self.db_name = db_name
        # 开启线程模式,支撑多线程执行
        self.conn = sqlite3.connect(self.db_name,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _get_beijing_time(self):
        """获取东八区时间"""
        utc_now = datetime.utcnow()
        beijing_time = utc_now + timedelta(hours=8)
        return beijing_time.strftime("%Y-%m-%d %H:%M:%S")

    def _create_tables(self):
        """创建表结构"""
        # 创建 report 表
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS report (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            project VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            run_time TEXT NOT NULL,
            passed INTEGER DEFAULT 0,
            failed INTEGER DEFAULT 0,
            skipped INTEGER DEFAULT 0,
            error INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', '+8 hours')),
            updated_at TEXT DEFAULT (datetime('now', '+8 hours'))
        )
        """
        )

        # 创建 api_detail 表
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS api_detail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            passed INTEGER DEFAULT 0,
            failed INTEGER DEFAULT 0,
            skipped INTEGER DEFAULT 0,
            error INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', '+8 hours')),
            updated_at TEXT DEFAULT (datetime('now', '+8 hours')),
            FOREIGN KEY (report_id) REFERENCES report(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
        )
        self.conn.commit()

    def insert_report(self, name, project, type, run_time, passed=0, failed=0, skipped=0, error=0):
        """插入数据到 report 表"""
        created_at = self._get_beijing_time()
        updated_at = created_at
        self.cursor.execute(
            """
        INSERT INTO report (name, project, type, run_time, passed, failed, skipped, error, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)
        """,
            (
                name,
                project,
                type,
                run_time,
                passed,
                failed,
                skipped,
                error,
                created_at,
                updated_at,
            ),
        )
        self.conn.commit()
        return self.cursor.lastrowid  # 返回最后插入的 report_id

    def insert_api_detail(self, report_id, name, passed=0, failed=0, skipped=0, error=0):
        """插入数据到 api_detail 表"""
        created_at = self._get_beijing_time()
        updated_at = created_at
        self.cursor.execute(
            """
        INSERT INTO api_detail (report_id, name, passed, failed, skipped, error, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (report_id, name, passed, failed, skipped, error, created_at, updated_at),
        )
        self.conn.commit()

    def fetch_failed_reports(self, report_id):
        """查询 最新的report是否存在fail数据"""
        self.cursor.execute("SELECT failed FROM report WHERE report_id = ?", (report_id,))
        result = self.cursor.fetchone()  # 使用 fetchone 获取单个值
        return result[0] if result and result[0] is not None else 0  # 处理 None 的情况

    def fetch_api_details_by_report(self, report_id):
        """根据 report_id 查询 api_detail 数据"""
        self.cursor.execute("SELECT * FROM api_detail WHERE report_id = ?", (report_id,))
        return self.cursor.fetchall()

    def fetch_api_detail(self, report_id):
        """根据 report_id 查询 api_detail 表中的 sum(failed) 值"""
        self.cursor.execute("SELECT sum(failed) FROM api_detail WHERE report_id = ?", (report_id,))
        result = self.cursor.fetchone()  # 使用 fetchone 获取单个值
        return result[0] if result and result[0] is not None else 0  # 处理 None 的情况

    def fetch_api_all(self, report_id):
        """根据 report_id 查询 api_detail 表中的所有值"""
        self.cursor.execute("SELECT count(1) FROM api_detail WHERE report_id = ?", (report_id,))
        result = self.cursor.fetchone()  # 使用 fetchone 获取单个值
        return result[0] if result and result[0] is not None else 0  # 处理 None 的情况

    def fetch_api_pass_all(self, report_id):
        """根据 report_id 查询 api_detail 表中的所有值"""
        self.cursor.execute("SELECT count(1) FROM api_detail WHERE report_id = ? and passed > 0 ", (report_id,))
        result = self.cursor.fetchone()  # 使用 fetchone 获取单个值
        return result[0] if result and result[0] is not None else 0  # 处理 None 的情况

    def update_report(self, report_id, failed=None):
        """
        根据 report_id 更新 report 表中的 failed 字段的值
        :param report_id: 需要更新的 report_id
        :param failed: 失败用例数（可选）
        :return: 受影响的行数
        """
        if failed is None:
            raise ValueError("`failed` 参数不能为空")
        sql = "UPDATE report SET failed = ? WHERE id = ?"
        try:
            self.cursor.execute(sql, (failed, report_id))
            self.conn.commit()  # 提交更改
            if self.cursor.rowcount != 0:
                # 额外调试：检查是否更新成功
                self.cursor.execute("SELECT failed FROM report WHERE id = ?", (report_id,))
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()  # 如果有异常，回滚事务
            raise e

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


ytest_db = YtestDatabase()

if __name__ == "__main__":
    # 创建数据库对象
    ic(ytest_db.update_report(24, 2))
