#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :api.py
@说明        :
@时间        :2022/02/14 11:21:13
@作者        :Leo
@版本        :1.0
"""
import requests, json, allure
from ytest.common.Logger import logger
from ytest.common.Allure import yallure


REQUESTS_LIST = ["GET", "POST", "PUT", "DELETE"]


class RequestInterface(object):
    def __init__(self):
        self.log = logger

    def __is_json(self, param: str) -> bool:
        try:
            json.loads(param)
        except ValueError:
            return False
        return True

    def __new_param(self, param):
        # 定义处理不同类型的请求参数、包含字典、字符串、空值
        if isinstance(param, str) and param.strip() == "":
            return None
        try:
            if isinstance(param, str) and self.__is_json(param):
                new_param = json.loads(param)
            elif param is None:
                new_param = ""
            else:
                new_param = param
        except Exception:
            new_param = ""
        return new_param

    def __validate_type(self, param, expected_types, param_name: str):
        if param is not None and not isinstance(param, tuple(expected_types)):
            expected_types_names = ", ".join([t.__name__ for t in expected_types])
            raise TypeError(f"参数 '{param_name}' 必须是 {expected_types_names} 类型中的一个, 但得到的是 {type(param).__name__}")

    def http_request(
        self,
        interface_domain: str,
        interface_api: str,
        interface_query: dict,
        interface_param: dict,
        request_type: str,
        headers: dict = None,
        cookies: dict = None,
    ):
        """
        统一处理http请求
        interface_url:接口地址
        interface_param：接口请求参数
        request_type:请求类型
        return 返回字典形式结果
        """
        # 先处理传入的参数，将空字符串转换为 None
        headers = self.__new_param(headers)
        cookies = self.__new_param(cookies)
        interface_query = self.__new_param(interface_query)
        interface_param = self.__new_param(interface_param)

        # 类型检查
        self.__validate_type(interface_domain, [str], "interface_domain")
        self.__validate_type(interface_api, [str], "interface_api")
        self.__validate_type(interface_query, [dict, list], "interface_query")
        self.__validate_type(interface_param, [dict, list], "interface_param")
        self.__validate_type(request_type, [str], "request_type")
        self.__validate_type(headers, [dict, None, ""], "headers")
        self.__validate_type(cookies, [dict, None, ""], "cookies")

        get_url = self.api_data(interface_api, "请求地址", interface_domain)
        self.log.info("步骤结束 -> 参数化数据处理成功")

        if get_url and request_type:
            if request_type.upper() in REQUESTS_LIST:
                self.log.info("步骤开始 -> 接口开始请求")
                result = self.__http(
                    type=request_type.upper(),
                    get_url=get_url,
                    headers=self.api_data(headers, "Headers") if headers else {},
                    cookies=self.api_data(cookies, "Cookies") if cookies else {},
                    interface_param=self.api_data(interface_query, "Param"),
                    interface_json=self.api_data(interface_param, "Body"),
                )
                return result
            else:
                raise ConnectionError("不支持的 request_type 参数")
        else:
            raise ConnectionError("get_url 或 request_type 参数为空")

    def __http(
        self,
        type: str,
        get_url: str,
        headers: dict,
        cookies: dict,
        interface_param: dict = None,
        interface_json: dict = None,
    ):
        if get_url:
            cookies = self.__new_param(cookies)
            headers = self.__new_param(headers)
            temp_interface_param = self.__new_param(interface_param)
            interface_json = self.__new_param(interface_json)
            if interface_json:
                response = requests.request(
                    type,
                    url=get_url,
                    params=temp_interface_param,
                    json=interface_json,
                    headers=headers,
                    cookies=cookies,
                )
            else:
                response = requests.request(
                    type,
                    url=get_url,
                    params=temp_interface_param,
                    headers=headers,
                    cookies=cookies,
                )
            self.api_data(response.text, "响应体")
            time_consuming = response.elapsed.microseconds / 1000
            time_total = response.elapsed.total_seconds()
            response_dicts = {
                "status_code": response.status_code,
                "body": self.__get_response_body(response),
                "text": response.text,
                "time_consuming": time_consuming,
                "time_total": time_total,
            }
            self.api_data(response.status_code, "状态码")
            return response_dicts

    def __get_response_body(self, response):
        try:
            return response.json()
        except ValueError:
            return response.text

    def api_data(self, data, desc, domain=None):
        if domain:
            data = domain + data
        allure.attach("{}".format(yallure.allure_data(data)), desc)
        return data


if __name__ == "__main__":
    ts = RequestInterface()
