#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :conf.py
@说明        :
@时间        :2023/04/28 17:33:08
@作者        :Leo
@版本        :1.0
"""

from configparser import ConfigParser
import sys
import os

log_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(log_path)
base_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(base_path)


# 用例基础配置
CASE_PATH = os.path.join(base_path, "case")


def find_file(folder, file_name):
    """
    判断文件是否存在
    Args:
        folder (path): 文件的绝对路径
        file_name (str): 需要判断的文件名
    Raises:
        FileNotFoundError: 文件不存在

    Returns:
        _type_: 返回存在文件的绝对路径
    """
    current_folder = os.path.abspath(folder)
    parent_folder = os.path.dirname(current_folder)

    # 在当前目录查找文件
    for root, dirs, files in os.walk(current_folder):
        if file_name in files:
            return os.path.join(root, file_name)

    # 在父目录查找文件
    for root, dirs, files in os.walk(parent_folder):
        if file_name in files:
            return os.path.join(root, file_name)

    # 文件不存在
    raise FileNotFoundError(f"{folder}目录及其父目录下,文件{file_name}不存在,请检查")


class Config:
    def __init__(self, project, conf=None):
        # 防止占位符给替换
        self.config = ConfigParser(interpolation=None)
        self.conf = f"{conf}.ini" if conf is not None else "default.ini"
        self.conf_path = find_file(os.path.join(CASE_PATH, project), self.conf)
        self.config.read(self.conf_path, encoding="utf-8")

    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def get_level(self):
        try:
            res = self.config.get("plan", "level")
        except Exception:
            res = None
        return res


if __name__ == "__main__":
    Ctest = Config("demo")
    test = Ctest.get_conf("mysql", "mysql_passwd")
    print(test)
