#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :public.py
@说明        :用例开始执行前,初始化的全局变量
                1.如果需要使用返回值必须return
                2.返回值如果是特定类型,必须指定类型
@作者        :Leo
@版本        :1.0
"""
import time


def timestamp_13():
    # 获取当前时间戳（秒级）
    current_time = time.time()
    # 将秒级时间戳转换为毫秒级时间戳
    timestamp_13_digits = int(current_time * 1000)

    return str(timestamp_13_digits)


def token():
    return "auto-test-123456789"


if __name__ == "__main__":
    print(timestamp_13())
