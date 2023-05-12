#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :setup.py
@说明        :
@时间        :2023/05/08 15:03:49
@作者        :Leo
@版本        :1.0
'''
from common.control import hook_variable
from utils.db import mysql
import re
import string

# 1. 先执行前置条件,执行完成后,再去校验header,body,query,url 是否存在${value}存在则更新返回
# 2. 前置/后置条件: 先更新里面的变量 2.再执行sql或者函数 3.执行结果再更新回全局变量


def func_run(func_list,global_variable):
    """
    前置条件执行func
    Args:
        func_list (list): 函数列表
        global_variable (dict): 全局变量表
    """
    if len(func_list)>0:
        for func in func_list:
            if func['type']=='func':
                value = func['func']
                func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", value)
                func_arg = value.split('(')[1].split(')')[0]
                    # 获取钩子函数名和变量名
                hook_list = hook_variable.get_hook_name()
                if func_arg:
                    # 替换参数中的变量名为实际值
                    func_arg = string.Template(func_arg).substitute(global_variable)
                    # 解析参数列表
                    kwargs = dict(l.replace(' ', '').split('=', 1) for l in func_arg.split(','))
                    # 调用钩子函数并获取返回值
                    result = hook_variable.get_hook_variable(hook_list, func_list[0], **kwargs)     
                else:
                    # 调用钩子函数并获取返回值
                    result = hook_variable.get_hook_variable(hook_list, func_list[0])
                if 'key' in func:
                    global_variable.update({func['key']:result})

              
def sql_run(sql_list,product,env,global_variable):
    """
    执行sql语句,暂时只支持mysql
    Args:
        sql_list (list): Excel中的sql语句
        product (str): 需要执行的项目
        env (str): 读取的sql配置信息文件
        global_variable (dict): 全局变量表
    """
    if len(sql_list)>0:
        for sql in sql_list:
            if sql['type']=='mysql':
                _sql = string.Template(sql['sql']).substitute(global_variable)
                DB = mysql.MysqlDb(sql['database'],product,env)
                result = DB.select_db(_sql)
                if 'key' in sql:
                    global_variable.update({sql['key']:result})



    
    