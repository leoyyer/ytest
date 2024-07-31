#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :request.py
@说明        :
@时间        :2022/02/14 11:21:13
@作者        :Leo
@版本        :1.0
'''
import requests
import json
import allure
import os
from utils.logger.logger import MyLog
from common.allure.allure_conf import allure_data
from common.control.exc import RequestInterfaceError
REQUESTS_LIST = ['GET', 'POST', 'PUT', 'DELETE']


class RequestInterface(object):
    def __init__(self):
        self.log = MyLog(logger_name=__name__)

    def __is_json(self, param):
        try:
            json.loads(param)
        except ValueError:
            return False
        return True

    def __new_param(self, param):
         # 定义处理不同类型的请求参数、包含字典、字符串、空值
        try:
            if isinstance(param, str) and self.__is_json(param):
                new_param = json.loads(param)
            elif param is None:
                new_param = ''
            else:
                new_param = param
        except Exception:
            new_param = ''
        return new_param

    def http_request(self, interface_domain, interface_api, interface_query, interface_param, request_type, headers, cookies):
        ''' 
        统一处理http请求
        interface_url:接口地址
        interface_param：接口请求参数
        request_type:请求类型
        return 返回字典形式结果
        '''
        try:
            get_url = self.api_data(interface_api, '请求地址', interface_domain)
            self.log.info("步骤结束 -> 参数化数据处理成功")
            if get_url != '' and request_type != '':
                if request_type.upper() in REQUESTS_LIST:
                    self.log.info("步骤开始 -> 接口开始请求")
                    result = self.__http(
                        type=request_type.upper(),
                        get_url=get_url,
                        headers=self.api_data(headers, 'Headers'),
                        cookies=self.api_data(cookies, 'Cookies'),
                        interface_param=self.api_data(interface_query, 'Param'),
                        interface_json=self.api_data(interface_param, '请求Body'))
            else:
                raise RequestInterfaceError("request_type参数错误")
        except Exception as e:
            raise RequestInterfaceError(f"系统异常,{e}")
        return result


    def __http(self, type, get_url, headers, cookies, interface_param=None, interface_json=None):
        try:
            if get_url:
                cookies = self.__new_param(cookies)
                headers = self.__new_param(headers)
                temp_interface_param = self.__new_param(interface_param)
                interface_json = self.__new_param(interface_json)
                if interface_json:
                    response = requests.request(type, url=get_url, params=temp_interface_param, json=interface_json, headers=headers, cookies=cookies)
                else:
                    response = requests.request(type, url=get_url, params=temp_interface_param, headers=headers, cookies=cookies)
                self.api_data(response.text, '响应体')
                time_consuming = response.elapsed.microseconds / 1000
                time_total = response.elapsed.total_seconds()
                response_dicts = dict()
                response_dicts['status_code'] = response.status_code
                self.api_data(response.status_code, '状态码')
                try:
                    response_dicts['body'] = response.json()
                    
                except Exception:
                    response_dicts['body'] = ''
                response_dicts['text'] = response.text
                response_dicts['time_consuming'] = time_consuming
                response_dicts['time_total'] = time_total
                return response_dicts
        except requests.RequestException as e:
            self.log.error('%s%s' % ('RequestException url: ', get_url))
            raise RequestInterfaceError(f"{type} 类型请求失败:{e}")

    def api_data(self, data, desc, domain=None):
        if domain:
            data = domain + data
        allure.attach('{}'.format(allure_data(data)), desc)
        return data


if __name__ == '__main__':
    ts = RequestInterface()
