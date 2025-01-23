#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :conf.py
@说明        :管理文件路径
@时间        :2024/08/15 18:29:31
@作者        :Leo
@版本        :1.0
"""

import os
from ytest.utils.case.case_file import find_folder
import sys


class Config:
    case_path = find_folder("case")
    ytest_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(case_path)
    sys.path.append(ytest_path)


config = Config()
