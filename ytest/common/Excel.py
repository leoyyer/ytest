#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :read_file.py
@说明        :
@时间        :2021/09/09 10:01:40
@作者        :Leo
@版本        :1.0
"""
import os, json, xlrd, re, string, jsonschema, pymysql
from ytest.common.Logger import logger
from ytest.common.HookVariable import hook_variable
from ytest.common.File import file_operate
from ytest.conf import config

from ytest.case.conftest import BLACK_LIST, GLOBAL_VARIABLE


class ReadXlsData:
    def __init__(self, filename: str):
        """[summary]
        初始化函数，用于读取 excel 文件
        Args:
            filename (str): excel 文件路径
        """
        self.filename = filename
        self.exl = self.get_filename(filename)
        self.case_excel = xlrd.open_workbook(filename)
        self.base_conf = self.get_base_data()
        self.global_variable = self.get_variable_data()
        self.get_black_list()
        self.get_expected_data()
        self.get_sql_detail()

    def table_rows(self, n: int) -> xlrd.sheet.Sheet:
        """
        获取指定 sheet 的表格对象
        Args:
            n (int): sheet 的索引
        Returns:
            xlrd.sheet.Sheet: 表格对象
        """
        table = self.case_excel.sheet_by_index(n)
        return table

    def get_filename(self, filename):
        """获取excel name"""
        # 判断excel文件是否存在
        if os.path.exists(filename):
            # 将excel文件名设置为全局变量consts.EXCEL
            # 通过os.path.split方法获取excel文件的路径和文件名
            dir_path, filename = os.path.split(filename)
            dir_list = os.path.normpath(dir_path).split(os.path.sep)
            case_name = filename.rsplit(".xlsx", 1)[0]
            NOW_EXCEL_DETAIL = {
                "file_name": filename,
                "case_name": case_name,
                "type": dir_list[-1],
                "project": dir_list[-2],
            }
            return NOW_EXCEL_DETAIL
        else:
            # 如果excel文件不存在，则抛出FileError异常
            raise FileNotFoundError(f"{filename} 不存在,请检查")

    def get_base_data(self):
        """获取base页数据"""
        try:
            # 获取第一个sheet中的所有行
            table = self.case_excel.sheet_by_index(0)
            base_data_dict = {}
            # 遍历所有行
            for n in range(0, table.nrows):
                # 获取当前行的第一个单元格的值作为字典的key, 获取当前行的第二个单元格的值作为字典的value
                base_data_dict.update({table.cell_value(n, 0): table.cell_value(n, 1)})
            self.exl.update({"base": base_data_dict})
            return base_data_dict
        except Exception as e:
            # 如果发生异常则抛出自定义异常CaseGenerateError并带上异常信息
            raise AttributeError(f"获取base数据失败,请检查:{e}")

    def get_black_list(self):
        """
        从case/coonftest.py中获取黑名单并更新到全局变量 BLACK_LIST 中
        """
        # 获取当前模块的名称
        exl = self.exl["case_name"]
        # 从配置文件中获取黑名单，以逗号分隔
        value = self.base_conf["blacklist"].split(",") if self.base_conf["blacklist"] else []
        # 将黑名单更新到全局变量 BLACK_LIST 中，以模块名和字段名为 key
        BLACK_LIST.update({f"{exl}_black_list": value})
        # 将黑名单更新到Base中，以模块名和字段名为 key
        self.exl["base"].update({"blacklist": value})
        # 返回更新后的全局变量
        return BLACK_LIST

    def get_expected_data(self):
        """从excel中获取公共断言数据并返回成一个以逗号分隔的字符串
        Args:
            self: 类对象本身
        Returns:
            str: 以逗号分隔的字符串
        Raises:
            CaseGenerateError: 如果出现任何错误，都会引发此异常
        """
        try:
            table = self.table_rows(3)  # 获取第三个表单的行数和列数
            result_list = []  # 存储所有合法的断言字典
            for n in range(1, table.nrows):
                assert_str = table.cell_value(n, 0)
                try:
                    assert_dict = json.loads(assert_str)  # 尝试将断言字符串转换为字典
                    result_list.append(assert_dict)
                except json.JSONDecodeError:
                    raise AttributeError(f"公共断言格式不正确,请检查: {assert_str}")  # 如果无法转换为字典，报异常
            result_str = ",".join(json.dumps(assert_dict) for assert_dict in result_list)
            self.exl["base"].update({"base_assert": result_list})
            return result_str
        except Exception as e:
            # 如果出现异常，则引发CaseGenerateError异常
            raise AttributeError(f"公共断言生成失败,请检查: {e}")

    def get_sql_detail(self):
        """解析excel中的sql,转换为字典"""
        try:
            table = self.table_rows(4)  # 获取第4个表单的行数和列数
            result_list = []  # 存储所有合法的断言字典
            for n in range(1, table.nrows):
                assert_str = hook_variable.resolve_vars(table.cell_value(n, 0), self.global_variable)
                # 确保 assert_str 是字符串类型
                if not isinstance(assert_str, str):
                    raise AttributeError(f"预期字符串类型, 但得到: {type(assert_str)}")
                try:
                    # 尝试将 sql 字符串转换为字典
                    assert_dict = json.loads(assert_str)
                    result_list.append({f"{n}": assert_dict})
                except json.JSONDecodeError:
                    raise pymysql.ProgrammingError(f"sql格式不正确,请检查: {assert_str}")
                    # 如果无法转换为字典，报异常
            self.exl["base"].update({"sql_list": result_list})
        except Exception as e:
            # 如果出现异常，则引发 CaseGenerateError 异常
            raise AttributeError(f"sql初始化失败,请检查: {e}")

    def target_exp_data(self, target_exp, exp):
        """
        将公共断言和自定义断言合并
        :param target_exp: 公共断言
        :param exp: 自定义断言
        :return: 合并后的断言字符串
        """
        pattern = r"\{.*?\}"
        # 使用正则表达式解析字符串，得到匹配的结果列表
        match_list = re.findall(pattern, exp)
        # 遍历结果列表，将每个字符串转换为字典，并添加到字典列表中
        result_list = []
        try:
            for match_str in match_list:
                match_dict = json.loads(match_str)
                result_list.append(match_dict)
            if result_list:
                # 合并
                expecte_list = result_list + target_exp
                # 去重
                expecte_list = list(set([tuple(d.items()) for d in expecte_list]))
                # 重组
                expecte_list = [dict(t) for t in expecte_list]
            else:
                expecte_list = target_exp
            return expecte_list
        except Exception as e:
            raise Exception(f"断言解析失败:{match_str} >>> {e}")

    def get_variable_data(self):
        """
        variable 变量池生成
        """
        # 获取变量表
        table = self.table_rows(2)
        type_converter = {
            "int": int,
            "list": lambda x: x.split(","),
            "string": str,
            "float": float,
            "func": self._get_hook_value,
        }
        try:
            # 遍历变量表中的每一行
            for n in range(1, table.nrows):
                var_type = table.cell_value(n, 2)
                if var_type:
                    if var_type in type_converter:
                        value = table.cell_value(n, 1)
                        try:
                            if var_type == "func":
                                value = type_converter[var_type](value)
                            else:
                                value = type_converter[var_type](value)
                            GLOBAL_VARIABLE[f"{table.cell_value(n, 0)}"] = value
                        except (ValueError, KeyError) as e:
                            logger.error(f"类型转换失败, 请检查变量表。变量类型: {var_type}, 变量值: {value}, 异常信息: {e}")
                            raise ValueError(f"类型转换失败, 请检查变量表。变量类型: {var_type}, 变量值: {value}, 异常信息: {e}")
                    else:
                        value = table.cell_value(n, 1)
                        try:
                            GLOBAL_VARIABLE[f"{table.cell_value(n, 0)}"] = json.loads(value)
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON 解析失败, 请检查变量表。变量类型: {var_type}, 变量值: {value}, 异常信息: {e}")
                            raise ValueError(f"JSON 解析失败, 请检查变量表。变量类型: {var_type}, 变量值: {value}, 异常信息: {e}")
        except (ValueError, KeyError) as e:
            logger.error(f"类型转换失败, 请检查变量表。异常信息: {e}")
            raise ValueError(f"类型转换失败, 请检查变量表。异常信息: {e}")

        # 返回更新后的全局变量池, 且更新全局变量到 base 中
        self.exl["base"].update({"global_variable": GLOBAL_VARIABLE})
        return GLOBAL_VARIABLE

    def _get_hook_value(self, value: str):
        """解析函数名和参数,执行函数,返回数据"""
        # 解析函数名和参数
        func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", value)
        func_arg = value.split("(")[1].split(")")[0]
        # 获取钩子函数名和变量名
        hook_list = hook_variable.get_hook_name(self.filename)
        if func_arg:
            # 替换参数中的变量名为实际值
            func_arg = string.Template(func_arg).substitute(GLOBAL_VARIABLE)
            # 解析参数列表
            kwargs = dict(l.replace(" ", "").split("=", 1) for l in func_arg.split(","))

            # 调用钩子函数并获取返回值
            return hook_variable.get_hook_variable(hook_list, func_list[0], **kwargs)
        else:
            # 调用钩子函数并获取返回值
            return hook_variable.get_hook_variable(hook_list, func_list[0])

    def get_case_data(self):
        """
        获取用例数据
        * 仅做数据读取,不做数据判断(is_run = 否,也正常读取,留给pytest判断是否要跳过)
        Returns:
            list: 完整的测试用例
        """
        table = self.table_rows(1)
        _len = table.nrows - 1
        self.exl["base"].update({"case_len": _len})
        case_list = []
        for n in range(1, table.nrows):
            # # 如果第二列为“否”,则跳过该行
            # if table.cell_value(n, 2) == '否':
            #     continue
            # 每行的所有单元格数据
            case_detail = {}
            update_dict = {
                0: (
                    "case_id",
                    hook_variable.resolve_vars(table.cell_value(n, 0), self.global_variable),
                ),
                1: (
                    "title",
                    hook_variable.resolve_vars(table.cell_value(n, 1), self.global_variable),
                ),
                2: (
                    "is_run",
                    hook_variable.resolve_vars(table.cell_value(n, 2), self.global_variable),
                ),
                3: (
                    "model",
                    hook_variable.resolve_vars(table.cell_value(n, 3), self.global_variable),
                ),
                4: (
                    "level",
                    hook_variable.resolve_vars(table.cell_value(n, 4), self.global_variable),
                ),
                5: (
                    "desc",
                    hook_variable.resolve_vars(table.cell_value(n, 5), self.global_variable),
                ),
                6: (
                    "domain",
                    (table.cell_value(n, 6) if table.cell_value(n, 6) else self.exl["base"]["base_url"]),
                ),
                7: (
                    "api",
                    hook_variable.resolve_vars(table.cell_value(n, 7), self.global_variable),
                ),
                8: ("method", table.cell_value(n, 8)),
                9: (
                    "headers",
                    hook_variable.str_to_dict(hook_variable.resolve_vars(table.cell_value(n, 9), self.global_variable)),
                ),
                10: (
                    "cookies",
                    hook_variable.str_to_dict(hook_variable.resolve_vars(table.cell_value(n, 10), self.global_variable)),
                ),
                11: (
                    "param",
                    hook_variable.str_to_dict(hook_variable.resolve_vars(table.cell_value(n, 11), self.global_variable)),
                ),
                12: (
                    "body",
                    hook_variable.str_to_dict(hook_variable.resolve_vars(table.cell_value(n, 12), self.global_variable)),
                ),
                13: (
                    "setup",
                    (self.update_sql_list(table, n, 13) if self.update_sql_list(table, n, 13) else []),
                ),
                14: (
                    "teardown",
                    (self.update_sql_list(table, n, 14) if self.update_sql_list(table, n, 14) else []),
                ),
                15: ("extract_data", self._extract_data(table, n, 15)),
                16: (
                    "expected_data",
                    self.target_exp_data(self.exl["base"]["base_assert"], table.cell_value(n, 16)),
                ),
                17: ("response", hook_variable.str_to_dict(table.cell_value(n, 17))),
                18: (
                    "black_list",
                    (str(table.cell_value(n, 18)).split(",") if table.cell_value(n, 18) else [] + self.exl["base"]["blacklist"]),
                ),
            }
            for i in update_dict:
                case_detail.update({update_dict[i][0]: update_dict[i][1]})
            case_list.append(case_detail)
        self.exl.update({"case_list": case_list})
        self.validate_case_data(self.exl)
        return self.exl

    def update_sql_list(self, table, m, n):
        """如果 setup, teardown 存在 sql，则合并 sql"""
        new_list = []
        cell_value = table.cell_value(m, n)

        if cell_value:  # 确保 cell_value 不为空
            if isinstance(cell_value, str):  # 确保 cell_value 是字符串类型
                try:
                    data = json.loads(cell_value)

                    if isinstance(data, dict) and data.get("type") == "sqllist":
                        sql_list = [i.strip() for i in data.get("num", "").split(",")]
                        for item in sql_list:
                            for key in self.exl["base"]["sql_list"]:
                                if item in key:
                                    new_list.append(self.exl["base"]["sql_list"][key[item]])
                    else:
                        # 确保 resolve_vars 返回的是字符串
                        resolved_value = hook_variable.resolve_vars(table.cell_value(m, n), self.global_variable)
                        if isinstance(resolved_value, str):
                            try:
                                _row = json.loads(resolved_value)
                                new_list.append(_row)
                            except json.JSONDecodeError:
                                new_list.append(resolved_value)
                        else:
                            new_list.append(resolved_value)
                except json.JSONDecodeError:
                    raise ValueError(f"Failed to parse JSON from cell value: {cell_value}")
            else:
                raise ValueError("Cell value is not a string and cannot be processed by json.loads")
        else:
            # print("Cell value is empty, returning an empty list.")
            # 如果 cell_value 为空，返回一个空列表
            return new_list

        return new_list

    def validate_case_data(self, case_data):
        """检验 case 是否符合模版"""
        json_schema = file_operate.find_file(config.ytest_path, "json_schema.json")
        with open(json_schema, "r") as f:
            json_schema = json.load(f)
        # 验证数据是否符合 JSON Schema
        try:
            jsonschema.validate(instance=case_data, schema=json_schema)
        except jsonschema.ValidationError as e:
            raise Exception(f"JSON Schema 验证失败: {e.message}")

    def _extract_data(self, table, m, n):
        """从表格中提取数据"""
        cell_value = table.cell_value(m, n)
        if cell_value:
            extract_list = [x for x in cell_value.split(";") if x.strip()]
        else:
            extract_list = []
        return extract_list


if __name__ == "__main__":
    excel = ReadXlsData("case/fast/suite/应用分析-概览.xlsx")
    case = excel.get_case_data()
    print(case)
