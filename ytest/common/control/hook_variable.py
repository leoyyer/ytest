#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :hook_variable.py
@说明        :
@时间        :2021/09/09 11:37:25
@作者        :Leo
@版本        :1.0
"""

import os
import re
import importlib
from ytest.common.control.exc import HookError, PathExtractionError


BASE_WORKDIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def extract_path(url):
    """_summary_
    1. 通过匹配(api|suite)获取到用例所在项目的路径
    2. 通过匹配(api|suite)获取到用例所在的项目

    Args:
        url (_type_): 测试用例的路径

    Raises:
        PathExtractionError: _description_

    Returns:
        _type_: _description_
    """
    # 使用正则表达式匹配包含`api`或`suite`的路径
    match = re.search(r"(.*/)(api|suite)/([^/]+)", url)

    if match:
        # 提取路径部分
        path = match.group(1)
        path_before_api_suite = os.path.normpath(path)

        # 提取path的最后一个文件夹
        folder = os.path.basename(path_before_api_suite)

        # 确保路径分隔符兼容Windows和Linux
        path = os.path.normpath(path)
        return path, folder
    else:
        # 如果无法匹配，抛出自定义异常
        raise PathExtractionError("无法从URL中提取到有效的路径和文件夹部分")


def get_hook_variable(list, funcName, **args):
    """
    1. 判断项目下是否存在hooks.py 文件,存在则装载到模块中
    2. 判断用例中所传入的函数是否存在于hook中,存在则执行

    Args:
        list (_type_): {"hook_list": hook_list, "project": folder}
        funcName (_type_): 函数名称

    Raises:
        HookError: _description_

    Returns:
        _type_: _description_
    """
    hooks = list["hook_list"]
    if len(hooks):
        for i in hooks:
            moduleSrc = f"case.{list['project']}." + i
            # 动态导入模块
            lib = importlib.import_module(moduleSrc)
            # 判断函数是否存在模块中
            if hasattr(lib, funcName):
                # 执行函数
                function = getattr(lib, funcName)
                return function(**args)
        else:
            raise HookError(f"函数{funcName}不存在,请检查.")


def get_hook_name(path):
    """
    1. 通过路径,找到路径下的py文件,作为模块记录下来
    Args:
        path (_type_): 项目路径
    Returns:
        _type_: 项目名以及项目下的所有hook文件
    """
    hook_path, folder = extract_path(path)
    filelist = os.listdir(hook_path)
    hook_list = []
    for item in filelist:
        # 输出指定后缀类型的文件
        if item.endswith(".py"):
            hook_list.append(item.split(".")[0])
    return {"hook_list": hook_list, "project": folder}


if __name__ == "__main__":
    list = get_hook_name("excel的绝对路径")
    kwargs = {"data": 3, "data2": "two"}
    test = get_hook_variable(list, "generate_overview_time_range", **kwargs)
    test2 = get_hook_variable(list, "auto_commit_file")
