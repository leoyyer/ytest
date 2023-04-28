#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(base_path)
import pytest
from common import log
from config import consts
from common.case import _assert
from common.case._params import _params
from common.api import request
from common.case.setupteardown import Setupteardownmethod
from common.read_file import ReadXlsData
from common._allure.allure_data import allure_data
from common._allure.allure_step import allure_step
import allure
from pathlib import Path
from common.env import now_conf



class TestSuite(object):
    log = log.MyLog()
    filename = str(Path(r'{{ filename }}'))
    data = ReadXlsData(filename)
    case_detail = data.get_case_data()
    case_list = case_detail[0]
    ids = [x[0] for x in case_detail[0]]

    # 执行用例前置操作（对应excel的set_up操作）
    def _setup(self, setup_data, param, setup_name=None):
        param = self.SetupTeardown.setup_public(setup_data, param, setup_name)
        self.log.info(f"步骤结束 <- 执行{setup_name}步骤成功")
        return param

    # 按excel每个用例依次传入并执行
    @allure.title("{title}")
    @pytest.mark.parametrize(*[case_list.keys()], [[case_list[key] for key in case_list]], ids=ids)
    def test_case(self, num, title, is_run, model, level, description, domain, api, restype, headers, cookies, query, param, setup_data, teardown_data, extract, expected_data, response_data, black_list, env):
        self.SetupTeardown = Setupteardownmethod(self.filename, env, self.case_list)
        self.request = request.RequestInterface(self.filename)
        self.case_assert = _assert.Assertions(self.filename, env)
        run_env = now_conf(self.filename, env)
        _level = run_env.get_level() if run_env.get_level() is not None else level
        domain = run_env.get_env(domain)
        if level == _level:
            # 动态载入pytest_html的description
            desc = description if description is not None else '暂无描述'
            allure.dynamic.description(desc)
            # 动态装载case的严重等级
            allure.severity(consts.CASE_SEVERITY[level])
            self.log.info(f"用例执行开始 ---> 执行用例: {num}: {title}")
            # 判断是否需要前置操作
            if setup_data:
                self.log.info("步骤开始 -> 存在前置步骤,执行前置步骤")
                setup_data = _params(setup_data, consts.GLOBAL_VARIABLE)
                allure_step('前置条件:', setup_data)
                self._setup(setup_data, param, setup_name="前置")
            # 接口请求
            # 对api、headers、入参进行参数化
            self.log.info("步骤开始 -> 处理参数化数据")
            response = self.request.http_request(interface_domain=domain, interface_api=api, headers=headers, cookies=cookies, interface_param=param, interface_query=query, request_type=restype)
            allure.attach('{}'.format(allure_data(response)), 'response')
            self.log.info("步骤结束 <- 请求成功,返回response")
            data = response
            # 断言结果
            if expected_data:
                allure.attach('{}'.format(allure_data(expected_data)), '断言')
                self.log.info("步骤开始 -> 存在断言,执行断言")
                assert self.case_assert.assert_method(data, expected_data)
                self.log.info("步骤结束 -> 断言完成")
            # 判断是否需要参数提取操作
            if extract:
                allure.attach('{}'.format(allure_data(extract)), '参数提取')
                # 后置操作:参数提取
                self.api_extract(data, extract)
            if teardown_data:
                self.log.info("步骤开始 -> 存在后置操作步骤,执行后置操作")
                self._teardown(teardown_data)
            allure.attach('{}'.format(allure_data(consts.GLOBAL_VARIABLE)), '全局变量表')
            self.log.info("用例执行结束 <--- 用例执行成功,更新全局变量表")
        else:
            pytest.skip("用例等级不符,直接跳过")

    # 参数提取操作
    def api_extract(self, response, param):
        self.log.info("步骤开始 -> 存在参数提取,执行参数提取")
        self.SetupTeardown.teardown_public(response, param)

    # 后置操作
    def _teardown(self, param):
        teardown_data = _params(param, consts.GLOBAL_VARIABLE)
        allure_step('后置操作:', teardown_data)
        self._setup(teardown_data, param, setup_name="后置")


if __name__ == '__main__':
    pytest.main(['-s', '-x', "-o", "log_cli=true", "-o", "log_cli_level=INFO", r'test_case/{{project}}/{{path}}/{{ case_name }}'])