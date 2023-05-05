#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :hook_variable.py
@说明        :
@时间        :2021/09/09 11:37:25
@作者        :Leo
@版本        :1.0
'''

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :Hook.py
@说明        :变量动态生成
@时间        :2021/07/13 10:16:21
@作者        :Leo
@版本        :1.0
'''
import os
import importlib
from common.control.exc import CustomError,HookError

BASE_WORKDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def get_hook_variable(list, funcName, **args):
    if len(list):
        try:
            for i in list:
                moduleSrc = 'hook.' + i
                # 动态导入模块
                lib = importlib.import_module(moduleSrc)
                # 判断函数是否存在模块中
                if hasattr(lib, funcName):
                    # 执行函数
                    function = getattr(lib, funcName)
                    return function(**args)
            else:
                raise HookError(f'函数{funcName}不存在,请检查.')
        except CustomError as e:
            raise HookError(f'函数{funcName}执行失败,请检查. Error:{e}')
    else:
        raise HookError(f'函数{funcName}不存在,请检查.')


def get_hook_name():
    filelist = os.listdir(BASE_WORKDIR + '/hook')
    hook_list = []
    for item in filelist:
        # 输出指定后缀类型的文件
        if(item.endswith('.py')):
            hook_list.append(item.split(".")[0])
    return hook_list


if __name__ == '__main__':
    list = get_hook_name()
    kwargs = {"data": 3, "data2": "two"}
    test = get_hook_variable(list, "test_hook", **kwargs)
    test2 = get_hook_variable(list, 'auto_commit_file')
