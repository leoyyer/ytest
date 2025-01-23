#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :setup.py
@说明        :
@时间        :2023/05/08 15:03:49
@作者        :Leo
@版本        :1.0
"""

from ytest.common.HookVariable import hook_variable
from ytest.common.Mysql import MysqlDb
import re, string, jsonpath
from ytest.common.Logger import logger


# 1. 先执行前置条件,执行完成后,再去校验header,body,query,url 是否存在${value}存在则更新返回
# 2. 前置/后置条件: 先更新里面的变量 2.再执行sql或者函数 3.执行结果再更新回全局变量


class SetupTearDown:
    def __init__(self) -> None:
        pass

    def func_run(self, url, func_list, global_variable):
        """
        前置条件执行func
        Args:
            func_list (list): 函数列表
            global_variable (dict): 全局变量表
        """
        if len(func_list) > 0:
            for func in func_list:
                if func["type"] == "func":
                    value = func["func"]
                    func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", value)
                    func_arg = value.split("(")[1].split(")")[0]
                    # 获取钩子函数名和变量名
                    hook_list = hook_variable.get_hook_name(url)
                    if func_arg:
                        # 替换参数中的变量名为实际值
                        func_arg = string.Template(func_arg).substitute(global_variable)
                        # 解析参数列表
                        kwargs = dict(l.replace(" ", "").split("=", 1) for l in func_arg.split(","))
                        # 调用钩子函数并获取返回值
                        result = hook_variable.get_hook_variable(hook_list, func_list[0], **kwargs)
                    else:
                        # 调用钩子函数并获取返回值
                        result = hook_variable.get_hook_variable(hook_list, func_list[0])
                    if "key" in func:
                        global_variable.update({func["key"]: result})

    def sql_run(self, case_data, sql_list, product, env, global_variable):
        """
        执行sql语句，暂时只支持mysql。

        Args:
            case_data (list): 包含需要执行的用例数据（从Excel读取的）。
            sql_list (list): 存储SQL语句和相关信息。
            product (str): 当前项目名。
            env (str): 当前环境名。
            global_variable (dict): 全局变量表，用于替换SQL中的变量。
        """
        # 如果case_data为空或sql_list为空，直接返回
        if not isinstance(case_data, list) or len(case_data) == 0:
            return
        if not isinstance(sql_list, list) or len(sql_list) == 0:
            return

        # 获取当前用例的SQL列表
        now_case_list = case_data[0].get("sql_list", [])
        if not now_case_list:
            return

        # 找到匹配的SQL语句
        _now_case_list = []
        for i in now_case_list:
            # 查找sql_list中包含当前用例的SQL
            matched_sql = next((s[i] for s in sql_list if i in s), None)
            if matched_sql:
                _now_case_list.append(matched_sql)

        if not _now_case_list:
            raise Exception("没有找到匹配的SQL语句")

        # 执行SQL语句
        for sql in _now_case_list:
            if sql.get("type") == "mysql":
                _sql = string.Template(sql["sql"]).substitute(global_variable)  # 替换SQL中的全局变量
                print(f"待执行SQL:{_sql}\n")

                # 执行数据库查询
                DB = MysqlDb(sql["database"], product, env)
                result = DB.select_db(_sql)

                # 如果SQL包含"key"，将结果保存到global_variable中
                if "key" in sql:
                    global_variable[sql["key"]] = result
                    print(f"将查询结果更新到全局变量: {sql['key']}\n")

    def extract(self, response, extract_param, global_variable):
        """
        参数提取,更新到全局变量
        """
        if not response:
            raise ValueError("无效的响应体")
        if len(extract_param):
            for extract in extract_param:
                _extract = {i.split("=")[0]: i.split("=")[1] for i in extract.split(";")}
                value = next(iter(_extract.values()))
                res = jsonpath.jsonpath(response, f"$.{value}")
                global_variable.update({next(iter(_extract.keys())): res[0]})
        print(f"[全局变量列表更新] >>> \n{global_variable}")


setupteardown = SetupTearDown()
