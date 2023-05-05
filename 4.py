#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :hook_variable.py
@说明        :
@时间        :2021/09/09 11:37:25
@作者        :Leo
@版本        :1.0
'''

import sys
import os
import importlib
from exc import HookError
from config import consts


def get_hook_variable(hook_list, func_name, **kwargs):
    """
    动态获取hook中指定函数的返回值

    :param hook_list: 一个包含hook文件名的列表
    :param func_name: 要获取的函数名
    :param kwargs: 传递给函数的参数
    :return: 函数的返回值
    """
    if len(hook_list):
        try:
            for hook in hook_list:
                module_src = 'hook.' + hook
                # 动态导入模块
                lib = importlib.import_module(module_src)
                # 判断函数是否存在模块中
                if hasattr(lib, func_name):
                    # 执行函数
                    function = getattr(lib, func_name)
                    return function(**kwargs)
            else:
                raise HookError(f'函数{func_name}不存在,请检查.')
        except HookError as e:
            raise HookError(f'函数{func_name}执行失败,请检查.', e)


def get_hook_name():
    """
    获取hook文件名列表

    :return: 包含hook文件名的列表
    """
    hook_list = []
    with os.scandir(consts.BASE_WORKDIR + '/hook') as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.py'):
                hook_list.append(os.path.splitext(entry.name)[0])
    return hook_list


if __name__ == '__main__':
    hook_list = get_hook_name()
    kwargs = {"data": 3, "data2": "two"}
    test = get_hook_variable(hook_list, "test_hook", **kwargs)
    test2 = get_hook_variable(hook_list, 'auto_commit_file')
