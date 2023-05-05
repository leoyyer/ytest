#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :SetupTeardown.py
@说明        :
@时间        :2021/07/13 16:17:47
@作者        :Leo
@版本        :1.0
'''
import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
import re
import string
import json
from common.db import mongodb_operate
from common.db import mysql_operate
from common import log, hook_variable
from common.exc import SQLExecuteError, ParameterextractError, SetupCaseError, SetupError, FuncError, MongoExecuteError
from common.case import _assert, _extract
from common.api import request
from config import consts
from libs.params import _params
import os
from typing import Dict, List, Any, Tuple
import mysql.connector
import ast


class Setupteardownmethod(object):

    def __init__(self, filename, env, case_list):
        self.env = env
        self.filename = filename
        self.n = case_list
        self.assert_ = _assert.Assertions(filename, env)
        self.log = log.MyLog()
        self.request = request.RequestInterface(filename)
        self.extract = _extract.ExtractData()
        self.excel_name = os.path.split(filename)[1].split('.')[0] + '_'
        self.project = filename.split('data' + os.sep)[1].split(os.sep)[0]

    def setup_public(self, setup_data, param, setup_name):
        '''
        封装前置操作:以json格式封装
            1、如果type=mysql，则执行SQL；
            2、如果字符串如果以case_开头，则执行用例
            3、字符串如果是变量名，将它的值添加到全局变量，可以$引用
        '''
        try:
            setup_list = self.get_lines(setup_data)
            param = param
            for i in range(0, len(setup_list)):
                setup_data = json.loads(setup_list[i])
                if setup_data:
                    # 1.内容为SQL，则执行SQL；
                    if setup_data["type"] == "mysql":
                        self.log.info(f"执行{setup_name}步骤[mysql]")
                        sql_list = setup_data.get('sql_list', [setup_data])
                        for sql in sql_list:
                            if hasattr(self, 'exec_sql'):
                                self.exec_sql(sql)
                            else:
                                self.log.warning("方法exec_sql未定义")
                    # 2、字符串如果以case_开头，则执行用例
                    elif setup_data["type"] == "case":
                        self.log.info(f"执行{setup_name}步骤:{setup_data['text']}")
                        if hasattr(self, 'exec_case'):
                            self.exec_case(setup_data)
                        else:
                            self.log.warning("方法exec_case未定义")
                    # 4、内容为mongodb，则执行SQL，将key添加到全局变量
                    elif setup_data["type"] == "mongodb":
                        self.log.info(f"执行{setup_name}步骤[mongodb]")
                        mongo_list = setup_data.get('mongo_list', [setup_data])
                        for mongo in mongo_list:
                            if hasattr(self, 'exec_mongo'):
                                self.exec_mongo(mongo)
                            else:
                                self.log.warning("方法exec_mongo未定义")
                    elif setup_data["type"] == "func":
                        if hasattr(self, 'exec_func'):
                            self.exec_func(setup_data)
                        else:
                            self.log.warning("方法exec_func未定义")
            return param
        except Exception as e:
            self.log.error(f"{setup_name}操作失败,setup={setup_data}")
            raise SetupError(f"{setup_name}操作失败,setup={setup_data}", e)

    def teardown_public(self, response: str, param: str) -> None:
        '''
        封装后置操作
        提取参数；格式：参数名 = 提取路径(以.分割)
        '''
        # 提取参数；格式：参数名 = 提取路径(以.分割)
        param_data: Dict[str, str] = {i.split("=")[0]: i.split("=")[1] for i in param.split(";")}
        try:
            for key, value in param_data.items():
                opr = self.extract.public_extract(response, value)
                e = {(self.excel_name + key): opr}
                consts.GLOBAL_VARIABLE.update(e)
            self.log.info("步骤结束 <- 参数提取成功,更新全局变量表")
        except Exception as e:
            self.log.error("参数提取失败，response={}，提取参数={}".format(response, param))
            raise ParameterextractError(f'参数提取失败，response={response}，提取参数={param}', e)

    def get_lines(self, data):
        try:
            lines = []
            open_brackets = 0
            start = 0
            is_comment = False
            for index, c in enumerate(data):
                if c == '"':
                    is_comment = not is_comment
                elif not is_comment:
                    if c == '{':
                        if not open_brackets:
                            start = index
                        open_brackets += 1

                    if c == '}':
                        open_brackets -= 1
                        if not open_brackets:
                            lines.append(data[start: index + 1])
            return lines
        except Exception as e:
            raise ParameterextractError(f'数据解析失败:{data}', e)

    def demo_api(self, num: int, title: str, domain: str, api: str, restype: str, headers: dict, cookies: dict,
                query: dict, param: str, expected_data: str, extract_data: str, setup_data: str, teardown_data: str):
        try:
            # 判断是否需要前置操作
            if setup_data:
                try:
                    setup_data = string.Template(_params(setup_data, self.excel_name)).substitute(consts.GLOBAL_VARIABLE)
                except Exception:
                    setup_data = setup_data
                self.setup_public(setup_data, param, "前置")

            # 对api、headers、query 入参进行参数化
            api = _params(api, self.excel_name)
            headers = _params(headers, self.excel_name)
            cookies = _params(cookies, self.excel_name)
            query = _params(query, self.excel_name)
            param = _params(param, self.excel_name)

            # 接口请求
            response = self.request.http_request(interface_domain=domain, interface_api=api, headers=headers,
                                                cookies=cookies, interface_param=param, interface_query=query,
                                                request_type=restype)

            # 断言结果
            if expected_data:
                self.log.info("当前Case存在断言,执行断言")
                assert self.assert_.assert_method(response, expected_data)

            # 参数提取
            if extract_data:
                self.teardown_public(response, extract_data)

            # 判断是否需要后置操作
            if teardown_data:
                self.log.info("当前Case存在后置处理,执行后置处理")
                try:
                    teardown_data = string.Template(param).substitute(consts.GLOBAL_VARIABLE)
                except Exception:
                    teardown_data = teardown_data
                self.setup_public(teardown_data, param, "后置")
            self.log.info("用例执行完成: %s: %s " % (num, title))
        except Exception as e:
            self.log.error("用例执行失败: %s: %s " % (num, title))
            raise SetupCaseError(f'用例执行失败:{num}-{title}', e)

    def exec_sql(self, data: Dict[str, Any]) -> None:
        """
        执行 SQL 语句
        Args:
            data: 包含数据库名、SQL 语句和参数提取规则的字典。
        Raises:
            SQLExecuteError: SQL 执行失败时抛出该异常。
            SetupCaseError: SQL 执行结果为空时，抛出该异常。
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)
            elif not isinstance(data, dict):
                raise ValueError(f"data 类型错误，必须是 str 或 dict 类型，当前类型：{type(data)}")

            self.log.info(f"步骤开始 -> 用例存在 SQL，执行 SQL：{data}")
            db = mysql_operate.MysqlDb(database=data["database"], project=self.project, env=self.env)
            sql_type = data["sql"].lower()
            if sql_type.startswith('select'):
                result = db.select_db(data["sql"])
                if "key" in data and len(result) > 0:
                    values = [item.get(key) for item in result for key in item]
                    key_name = self.excel_name + data["key"]
                    consts.GLOBAL_VARIABLE[key_name] = str(values[0])
                    self.log.info(f"步骤结束 <- SQL 执行成功，更新全局变量：{key_name}={values[0]}")
                elif not result:
                    raise SetupCaseError("SQL 执行结果为空，参数提取失败")
            elif sql_type.startswith('delete') or sql_type.startswith('update') or sql_type.startswith('insert'):
                db.execute_db(data["sql"])
            else:
                raise ValueError(f"不支持的 SQL 语句类型：{sql_type}")

            self.log.info("SQL 执行成功")
        except json.JSONDecodeError as e:
            self.log.error(f"SQL 数据解析失败，数据格式不是 JSON 格式：{data}")
            raise SQLExecuteError(f"SQL 数据解析失败，数据格式不是 JSON 格式：{data}", e)
        except ValueError as e:
            self.log.error(str(e))
            raise SQLExecuteError(str(e), e)
        except mysql.connector.Error as e:
            self.log.error(f"SQL 执行失败，请检查 SQL 语句或数据库配置：{data}")
            raise SQLExecuteError(f"SQL 执行失败，请检查 SQL 语句或数据库配置：{data}", e)
        except Exception as e:
            self.log.error(f"SQL 执行失败，请检查 SQL 语句或数据库配置：{data}")
            raise SQLExecuteError(f"SQL 执行失败，请检查 SQL 语句或数据库配置:{data}", e)

    def get_related_cases(self, setup_data: Dict[str, Any]) -> List[Tuple[str, str, str, str]]:
        """
        获取前置用例列表
        Args:
            setup_data (Dict[str, Any]): 前置用例信息

        Raises:
            SetupError: 前置用例不存在

        Returns:
            List[Tuple[str, str, str, str]]: 前置用例列表
        """
        target_case_list = [(num, title, domain, api) for num, title, domain, api in self.n if num == setup_data["text"]]
        if not target_case_list:
            self.log.error("{0}用例不存在,请检查.".format(setup_data["text"]))
            raise SetupError('{0}用例不存在,请检查。'.format(setup_data["text"]))
        else:
            return target_case_list

    def exec_case(self, setup_data):
        """
        1. case 必须存在于excel中,且已经启动
        2. 目前只支持一个case传入
        3. 传入格式:{"type":"case","text":"case_num"}

        Args:
            setup_data ([type]): [description]
        """
        case_list = self.get_related_cases(setup_data)
        for case in case_list:
            num, title, domain, api, _, headers, cookies, query, request_param, setup_data, expected_data, extract_data, teardown_data = case
            self.demo_api(num=num, title=title, domain=domain, api=api, headers=headers, cookies=cookies, query=query, request_param=request_param, expected_data=expected_data, extract_data=extract_data, setup_data=setup_data, teardown_data=teardown_data)

    def exec_mongo(self, mongo_data):
        """执行 MongoDB 操作。

        Args:
            mongo_data (dict): MongoDB 操作的相关参数。

        Raises:
            MongoExecuteError: MongoDB 执行失败时抛出该异常。

        """
        try:
            mongo_data = json.loads(string.Template(json.dumps(mongo_data)).substitute(consts.GLOBAL_VARIABLE))
            collectionMongo = mongodb_operate.CollectionMongo(database=mongo_data["database"], project=self.project, env=self.env)
            if mongo_data["method"] == "find":
                result = collectionMongo.find(collection=mongo_data["collection"], condition=json.loads(mongo_data["condition"]), column=str(mongo_data["column"]))
                result_list = [i for i in result]
                if ("key" in mongo_data):
                    c = [item[key] for item in result_list for key in item]
                    a = {(self.excel_name + mongo_data["key"]): str(c[0])}
                    consts.GLOBAL_VARIABLE.update(a)
                    self.log.info('mongo执行成功,更新全局变量')
            elif mongo_data["method"] == "insert_many":
                collectionMongo.insert_many(collection=mongo_data["collection"], data=mongo_data["data"])
            elif mongo_data["method"] == "update":
                collectionMongo.update(collection=mongo_data["collection"], data=json.loads(mongo_data["data"]))
            elif mongo_data["method"] == "delete":
                collectionMongo.delete(collection=mongo_data["collection"], condition=json.loads(mongo_data["condition"]))
        except Exception as e:
            self.log.error(f"mongodb执行失败,请检查:{mongo_data}")
            raise MongoExecuteError(f'数据库失败,请检查传入数据:{mongo_data}', e)
      
    def exec_func(self, data):
            """[summary]
            执行函数
            Args:
                data ([type]): [description]
            """
            try:
                func_list = re.findall(r"(?<=\$\{)(.*)(?=\()", data['func'])
                func_arg = data['func'].split('(')[1].split(')')[0]
                hook_list = hook_variable.get_hook_name()
                if func_arg:
                    func_arg = string.Template(_params(func_arg, self.excel_name)).substitute(consts.GLOBAL_VARIABLE)
                    kwargs = dict(l.replace(' ', '').split('=', 1) for l in func_arg.split(','))
                    value = hook_variable.get_hook_variable(hook_list, func_list[0], **kwargs)
                else:
                    value = hook_variable.get_hook_variable(hook_list, func_list[0])
                consts.GLOBAL_VARIABLE.update({(self.excel_name + data["key"]): value})
            except Exception as e:
                raise FuncError(f"函数:{data}执行失败,{e}")
