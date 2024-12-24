#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :conf.py
@说明        :
@时间        :2024/12/23 16:41:52
@作者        :Leo
@版本        :1.0
"""

import os, sys
from ytest.common.File import Flile


class Config:
    ytest_file = Flile()
    # 获取case文件夹路径
    case_path = ytest_file.find_folder("base")
    # 获取ytest项目路径
    ytest_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(case_path)
    sys.path.append(ytest_path)


config = Config()
