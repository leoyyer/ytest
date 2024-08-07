#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :_time.py
@说明        :
@时间        :2023/07/28 18:48:02
@作者        :Leo
@版本        :1.0
"""

from datetime import datetime


def _time():
    current_time = datetime.now()
    # 格式化为 20231001180501 的格式
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")
    return str(formatted_time)
