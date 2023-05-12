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

# 项目基础路径
BASE_WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# 用例基础配置
CASE_PATH = os.path.join(BASE_WORKDIR, "case")

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
    
    for root, dirs, files in os.walk(folder):
        if file_name in files:
            return os.path.join(root, file_name)
    raise FileNotFoundError(f'{folder}目录下,文件{file_name}不存在,请检查')


def get_file_path(folder, file=None):
    """
    判断项目中是否存在测试用例和ini配置文件,返回case_list
    folder: project 的绝对路径
    file: 
         None: 遍历整个project下的目录,返回case_list
         str["api","suite"]:遍历project/str下的目录,返回case_list
    """
    # 判断是否存在.ini文件
    ini_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.ini')]
    if not ini_files:
        raise Exception(f'{folder} 下,ini 配置文件不存在,请检查')
    
    if file is None:
        # 遍历folder下的全部文件夹，筛选出.xlsx文件
        case_list = []
        for root, dirs, files in os.walk(folder):
            for name in files:
                if name.endswith('.xlsx') and '_stop' not in name and '._' not in name:
                    case_list.append(os.path.join(root, name))
    else:
        # 判断路径是否存在
        path = os.path.join(folder, file)
        if not os.path.exists(path):
            raise Exception(f'{folder} 下, 文件 {file} 不存在,请检查')
        
        # 遍历路径下的全部文件夹，筛选出.xlsx文件
        case_list = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.xlsx') and '_stop' not in name and '._' not in name:
                    case_list.append(os.path.join(root, name))
    if len(case_list):
        return case_list
    else:
        raise Exception(f'{folder} 下不存在测试用例,请检查')

