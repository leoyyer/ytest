#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :assert.py
@说明        :
@时间        :2023/05/09 11:51:38
@作者        :Leo
@版本        :1.0
"""

from ytest.utils.logger.logger import MyLog
from ytest.utils.db import mysql
import string
from ytest.common.control import hook_variable
import jsonpath
import re
from ytest.common.control.exc import CaseError, AssertError
from ytest.common.control.replace_variable import resolve_vars


class Assertions:
    def __init__(self, project, env, global_variable):
        self.log = MyLog(logger_name=__name__)
        self.project = project
        self.env = env
        self.global_variable = global_variable

    def assert_method(self, data, expected_data_list):
        # 断言参数处理
        if len(expected_data_list):
            try:
                for item in expected_data_list:
                    # 存在${value}时,则替换变量的值
                    i = resolve_vars(item, self.global_variable)
                    if i["type"] == "response_body":
                        self.log.info(
                            "进入断言 -> (response_body)验证response body中任意属性的值"
                        )
                        assert self.assert_body(data, i["text"])
                        continue
                    elif i["type"] == "response_code":
                        code = data["status_code"]
                        self.log.info("进入断言 -> (response_code)验证response状态码")
                        assert self.assert_code(code, i["text"])
                        continue
                    elif i["type"] == "response_incloud":
                        self.log.info(
                            "进入断言 -> (response_incloud)验证response body中是否包含预期字符串"
                        )
                        assert self.assert_in_text(data, i["text"])
                        continue
                    elif i["type"] == "response_not_incloud":
                        self.log.info(
                            "进入断言 -> (response_not_incloud)验证response body中是不否包含预期字符串"
                        )
                        assert self.assert_not_in_text(data, i["text"])
                        continue
                    elif i["type"] == "length_equals":
                        assert self.length_equals(data, i)
                        continue
                    elif i["type"] == "time":
                        self.log.info(
                            "进入断言 -> (time)验证response body响应时间小于预期最大响应时间,单位：毫秒"
                        )
                        assert self.assert_time(data["time_total"], i["text"])
                        continue
                    elif i["type"] == "mysql":
                        self.log.info(
                            "进入断言 -> (mysql)验证返回数据是否与数据库相一致"
                        )
                        assert self.assert_sql(i)
                        continue
                    elif i["type"] == "mongodb":
                        self.log.info(
                            "进入断言 -> (mongodb)验证返回数据是否与数据库相一致"
                        )
                        assert self.assert_mongo(i)
                        continue
                return True
            except Exception as e:
                self.log.error(f"断言失败 {e}")
                return False
        else:
            self.log.info("不存在断言")
            return True

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:response.code
        :param expected_code: {"type":"response_code","text":"200"}
        :return:
        """
        try:
            assert str(code) == str(expected_code)
            self.log.info("assert_code 断言 -> 断言成功")
            return True
        except Exception as e:
            self.log.error(
                "断言失败 <- expected_code is %s, statusCode is %s "
                % (expected_code, code)
            )
            raise AssertError(f"response状态码断言失败,{e}")

    def assert_body(self, body, expected_data):
        """
        验证response body中任意属性的值
        :param body: response的body
        :param expected_data:(断言语句){'type': 'response_body', 'text': 'code=2000;msg=成功'}
        :return:
        """
        try:
            expected_data = {
                i.split("=")[0]: i.split("=")[1] for i in expected_data.split(";")
            }
            for key, value in expected_data.items():
                realdata = jsonpath.jsonpath(body["body"], key)
                if str(realdata[0]) == str(value):
                    result = True
                    self.log.info("assert_body 断言 -> 断言成功")
                    continue
                else:
                    result = False
                    self.log.error(
                        "assert_body 断言失败 <- %s实际返回值:%s, %s预期值:%s "
                        % (key, realdata[0], key, value)
                    )
                    break
            return result
        except Exception as e:
            self.log.error(f"断言数据解析失败 <- data:{expected_data}, error:{e}")
            raise AssertError(f"断言失败,{e}")

    def assert_in_text(self, body, expected_data):
        """
        验证response body中是否包含预期字符串
        :param body: response
        :param expected_msg:{"type":"response_incloud","text":"msg in 请与容器云（天眼）确认是否已配置采集应用基础监控信息"}
        :return:
        """
        try:
            expected_data = {
                i.split(" in ")[0]: i.split(" in ")[1] for i in expected_data.split(";")
            }
            for key, value in expected_data.items():
                realdata = jsonpath.jsonpath(body["body"], key)
                if str(value) in str(realdata[0]):
                    result = True
                    self.log.info("assert_in_text 断言 -> 断言成功")
                    continue
                else:
                    self.log.error(
                        "断言失败  <- %s实际返回值:%s, %s预期值:%s "
                        % (key, realdata[0], key, value)
                    )
                    result = False
            return result
        except Exception as e:
            self.log.error(f"断言数据解析失败 <- data:{expected_data}, error:{e}")
            raise AssertError(f"断言失败,{e}")

    def assert_not_in_text(self, body, expected_data):
        """
        验证response body中不包含预期字符串
        :param body:
        :param expected_msg: {"type":"response_incloud","text":"msg not_in 请与容器云（天眼）确认是否已配置采集应用基础监控信息"}
        :return:
        """
        try:
            expected_data = {
                i.split(" not_in ")[0]: i.split(" not_in ")[1]
                for i in expected_data.split(";")
            }
            for key, value in expected_data.items():
                realdata = jsonpath.jsonpath(body["body"], key)
                if str(value) not in str(realdata[0]):
                    result = True
                    self.log.info("assert_not_in_text 断言 -> 断言成功")
                    continue
                else:
                    self.log.error(
                        "断言失败 <- %s实际返回值:%s, %s预期值:%s "
                        % (key, realdata[0], key, value)
                    )
                    result = False
            return result
        except Exception as e:
            self.log.error(f"断言数据解析失败 <- data:{expected_data}, error:{e}")
            raise AssertError(f"断言失败,{e}")

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            self.log.info("assert_text断言 -> 断言成功")
            return True
        except Exception as e:
            self.log.error(
                "断言失败 <- Response body != expected_msg, expected_msg is %s, body is %s"
                % (expected_msg, body)
            )
            raise AssertError(f"断言失败,{e}")

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        try:
            assert eval(expected_time.replace("time", time))
            self.log.info("assert_time 断言 -> 断言成功")
            return True
        except Exception as e:
            self.log.error(
                "断言失败 <- Response time > expected_time, expected_time is %s, time is %s"
                % (expected_time, time)
            )

            raise AssertError(f"断言失败,{e}")

    def length_equals(self, body, expected_data):
        """
        expected_data 格式:
        1. 支持 body提取,比对: {"type":"length_equals","text":"res=body.items","len":1 }
        2. 支持 mysql查询,比对: {"type":"length_equals","text":"res=body.items", "database":"starship_test_ops","sql":"select count(*) from xxxxx where xxxxx"}
        3. 支持 函数返回值与body,比对: {"type":"length_equals","text":"res=body.items", "func":"${create_app_code()}"}
        """
        _expect = {
            i.split("=")[0]: i.split("=")[1] for i in expected_data["text"].split(";")
        }
        if len(_expect) == 1:
            value = next(iter(_expect.values()))
            res = jsonpath.jsonpath(body, f"$.{value}")
            if isinstance(res, list):
                if "len" in expected_data:
                    self.log.info(
                        "预期值: {0}, 实际返回值: {1}".format(
                            expected_data["len"], len(res)
                        )
                    )
                    assert len(res) == int(expected_data["len"])
                    self.log.info("assert_body 断言 -> 断言成功")
                    return True
                elif "database" in expected_data:
                    _sql = resolve_vars(expected_data["sql"], self.global_variable)
                    db = mysql.MysqlDb(
                        database=expected_data["database"],
                        project=self.project,
                        env=self.env,
                    )
                    result = db.select_db(_sql) if db.select_db(_sql) else "None"
                    self.log.info(f"执行sql, 返回结果: {result}")
                    if len(result) > 0:
                        sql_len = int(result[0][list(result[0].keys())[0]])
                        self.log.info(
                            "预期值: {0}, sql实际返回值: {1}".format(len(res), sql_len)
                        )
                        assert int(len(res)) == int(sql_len)
                        return True
                    else:
                        self.log.info(
                            "预期值: {0}, sql实际返回值: {1}".format(len(res), 0)
                        )
                        assert int(len(res)) == 0
                        return True
                elif "func" in expected_data:
                    func_list = re.findall(
                        r"(?<=\$\{)(.*)(?=\()", expected_data["func"]
                    )
                    _func_arg = expected_data["func"].split("(")[1].split(")")[0]
                    func_arg = string.Template(_func_arg).substitute(
                        self.global_variable
                    )
                    hook_list = hook_variable.get_hook_name()
                    if func_arg:
                        kwargs = dict(
                            l.replace(" ", "").split("=", 1)
                            for l in func_arg.split(",")
                        )
                        value = hook_variable.get_hook_variable(
                            hook_list, func_list[0], **kwargs
                        )
                    else:
                        value = hook_variable.get_hook_variable(hook_list, func_list[0])
                    assert int(len(res)) == int(value)
                    self.log.info(
                        "预期值: {0}, 函数实际返回值: {1}".format(len(res), value)
                    )
                    return True
            else:
                self.log.error("断言失败,提取的内容并非列表,无法进行断言")
                return False
        else:
            self.log.error("断言数据解析失败,格式错误,length_equals:text只支持一个参数")
            raise AssertError(
                "断言数据解析失败,格式错误,length_equals:text只支持一个参数"
            )

    def assert_sql(self, expected_data):
        """
        验证data不等于预期
        :param data:
        :param expected_data:
        :return:
        """
        try:
            db = mysql.MysqlDb(
                database=expected_data["database"], project=self.project, env=self.env
            )
            # self.log.info("sql连接成功,开始进入sql断言")
            try:
                c = (
                    db.select_db(expected_data["sql"])
                    if db.select_db(expected_data["sql"])
                    else "None"
                )
                self.log.info(f"sql执行结果: {c}")
                # 断言处理
                expectedresult = expected_data["text"].split("=")
                if expectedresult[0] == "result":
                    realdata = str(c).replace(" ", "")
                    expectedresult = expected_data["text"].split("=")
                    res = expectedresult[1]
                    # self.log.info(f"预期值: {realdata}")
                    # self.log.info(f"result实际返回值: {res}")
                    assert realdata == res.replace(" ", "")
                else:
                    expected_data_dict = {
                        i.split("=")[0]: i.split("=")[1]
                        for i in expected_data["text"].split(";")
                    }
                    for key, value in expected_data_dict.items():
                        i = re.findall("[[](.*?)[]]", key, re.I | re.M)[0]
                        finally_key = key.split(".")[-1]
                        realdata = self.find(finally_key, c[int(i)])
                        # self.log.info(f"{key}预期值: {value}")
                        # self.log.info(f"{key}实际返回值: {realdata}")
                        assert str(realdata).replace(" ", "") == str(value).replace(
                            " ", ""
                        )
                        # self.log.info(f"{key}断言成功")
                        self.log.info("mysql 断言 -> 断言成功")
                        # self.log.info("--------------------------------------------------------")
                # self.log.info("断言成功,进入下一个步骤")
                return True
            except AssertionError:
                self.log.error("expected_data is %s" % (expected_data))
                return False
        except Exception as e:
            self.log.error("数据库连接失败: %s" % (e))
            raise AssertError(f"断言失败,{e}")

    def find(self, target, dictData, notFound="没找到"):
        # 查找单个键
        queue = [dictData]
        while len(queue) > 0:
            data = queue.pop()
            for key, value in data.items():
                if key == target:
                    return value
                elif type(value) == dict:
                    queue.append(value)
        return notFound

    def findAll(self, target, dictData, notFound=[]):
        # 有多个同名键在字典里时，可以用这个方法
        queue = [dictData]
        result = []
        while len(queue) > 0:
            data = queue.pop()
            for key, value in data.items():
                if key == target:
                    result.append(value)
                elif type(value) == dict:
                    queue.append(value)
        if not result:
            result = notFound
        return result

    # 用于diff,暂时废弃
    def _assert_json_diff(self, new_resp, old_resp, clist):
        try:
            diff_list = []
            new_resp = new_resp["body"]
            g_black_list = consts.BLACK_LIST[self.excel_name + "black_list"]
            new_resp = self.update_dict(new_resp, g_black_list, clist)
            old_resp = self.update_dict(old_resp, g_black_list, clist)
            result = json_tools.diff(new_resp, old_resp)
            if len(result):
                for i in result:
                    # 目前只考虑diff结构体，add 和 remove，不校验值
                    if "remove" in i or "add" in i:
                        diff_list.append(i)
                if len(diff_list):
                    return False, diff_list
                else:
                    return False, ""
            else:
                return True, ""
        except Exception as e:
            raise AssertError(f"diff失败,{e}")

    # 用于diff,暂时废弃
    def update_dict(self, arg, g_list, clist):
        new_list = [x for x in list(set(clist + g_list)) if x != ""]
        if len(new_list):
            for i in new_list:
                parser = parse(i)
                try:
                    arg = parser.update(arg, "")
                except:
                    arg = arg
        return arg


if __name__ == "__main__":
    data = Assertions("demo", "test", {})
    data.assert_sql(
        {
            "type": "mysql",
            "database": "api_test_starship_branch",
            "sql": "select id from feature where id= '39ffd37b-6be7-db7d-072b-5bc325074bdb'",
            "text": "result=[{'id': '39ffd37b-6be7-db7d-072b-5bc325074bdb'}]",
        }
    )
    data.assert_sql(
        {
            "type": "mysql",
            "database": "api_test_starship_branch",
            "sql": "select id,name from feature where id= '39ffd37b-6be7-db7d-072b-5bc325074bdb'",
            "text": "result[0].id=39ffd37b-6be7-db7d-072b-5bc325074bdb",
        }
    )
