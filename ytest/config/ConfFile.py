#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :conf.py
@说明        : case运行时,读取case的配置文件
@时间        :2024/12/20 16:44:40
@作者        :Leo
@版本        :1.0
"""
from typing import Optional
from configparser import ConfigParser, NoOptionError, NoSectionError
import os
from ytest.common.File import file_operate
from ytest.conf import config


class ConfigFile:
    def __init__(self, project, conf: Optional[str] = None):
        """
        获取项目的配置文件(ini),如果没有,则去默认配置(default.ini)
        """
        # 防止占位符给替换
        self.config = ConfigParser(interpolation=None)
        self.conf: str = f"{conf}.ini" if conf is not None else "default.ini"
        self.conf_path = file_operate.find_file(os.path.join(config.case_path, project), self.conf)
        self.config.read(self.conf_path, encoding="utf-8")

    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def get_level(self) -> Optional[str]:
        try:
            res = self.config.get("plan", "level")
        except (NoOptionError, NoSectionError):
            res = None
        return res
