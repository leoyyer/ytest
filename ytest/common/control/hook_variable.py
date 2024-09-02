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
import sys
from ytest.utils.conf import config
from pathlib import Path


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


def get_hook_variable(hook_data, funcName, **args):
    """
    1. 判断项目下是否存在 hooks.py 文件，存在则装载到模块中
    2. 判断用例中所传入的函数是否存在于 hook 中，存在则执行

    Args:
        hook_data (dict): 包含 "hook_list" 和 "project" 的字典
        funcName (str): 函数名称

    Raises:
        HookError: 当函数不存在于模块中时抛出此异常

    Returns:
        Any: 函数执行后的返回值
    """
    hooks = hook_data.get("hook_list", [])
    project = hook_data.get("project")

    if not project:
        raise HookError("未指定项目名称。")

    # 使用 pathlib 处理路径，确保跨平台兼容性
    case_path = Path(config.case_path).resolve()
    case_parent_dir = case_path.parent

    # 将 case 的父目录添加到 sys.path 中，以便 Python 能找到 'case' 包
    case_parent_dir_str = str(case_parent_dir)
    if case_parent_dir_str not in sys.path:
        sys.path.append(case_parent_dir_str)

    if hooks:
        for hook in hooks:
            # 构建模块路径，如 "case.project.hook"
            moduleSrc = f"case.{project}.{hook}"
            try:
                # 动态导入模块
                lib = importlib.import_module(moduleSrc)
            except ModuleNotFoundError as e:
                raise HookError(f"模块 {moduleSrc} 未找到，请检查。") from e

            # 判断函数是否存在于模块中
            if hasattr(lib, funcName):
                function = getattr(lib, funcName)
                return function(**args)
        else:
            raise HookError(f"函数 {funcName} 不存在，请检查。")
    else:
        raise HookError("hooks 列表为空，请检查传入参数。")


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
