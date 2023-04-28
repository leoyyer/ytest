#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :conftest.py
@说明        :
@时间        :2023/04/24 17:56:49
@作者        :Leo
@版本        :1.0
'''
import os
import pytest

BLACK_LIST = {}
GLOBAL_VARIABLE ={}
NOW_EXCEL_DETAIL = {}

@pytest.fixture(scope="session")
def global_variable():
    """预设一些全局变量"""
    return {'GLOBAL_VARIABLE': GLOBAL_VARIABLE}


@pytest.fixture(scope="session")
def global_black_list():
    """
    使用diff功能时,全局过滤一些不需要diff的字段
    """
    return BLACK_LIST


def find_json_schema_file(folder, file_name):
    for root, dirs, files in os.walk(folder):
        if 'json_schema.json' in files:
            return os.path.join(root, file_name)
    raise FileNotFoundError('文件夹中不存在json_schema.json文件')