#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :Time.py
@说明        :
@时间        :2024/12/23 17:18:52
@作者        :Leo
@版本        :1.0
"""
from datetime import datetime


class Time:
    def __init__(self) -> None:
        pass

    def convert_to_month_day(self, timestamp):
        # 将时间戳字符串转换为datetime对象
        dt = datetime.strptime(str(timestamp), "%Y%m%d%H%M%S")
        # 格式化日期时间为指定格式
        formatted_date = dt.strftime("%m%d")
        return formatted_date

    def _time(self):
        current_time = datetime.now()
        # 格式化为 20231001180501 的格式
        formatted_time = current_time.strftime("%Y%m%d%H%M%S")
        return str(formatted_time)

    def _dateTime(self):
        # 获取当前时间
        now = datetime.now()
        # 输出结果
        now_date_time = now.strftime("%Y%m%d")
        # 例如：20241108
        return now_date_time


ytest_time = Time()
