#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pytest
import allure
import argparse
from ytest.common.conf.conf import Config
from ytest.common.control.read_xlsx import ReadXlsData
from ytest.utils.logger.logger import MyLog
from ytest.utils.case import setupteardown
from ytest.common.control.replace_variable import resolve_vars
from ytest.utils.api.request import RequestInterface
from ytest.utils.assertions.asserts import Assertions
from ytest.utils.extract.extracts import extract
from ytest.utils.tools._time import _time

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help="配置所需执行的用例路径")
parser.add_argument("--conf", type=str, help="配置指定的执行文件", default="default")
args = parser.parse_args()
log = MyLog(logger_name=__name__)


class TestSuite(object):
    # args.filename = "调试入口,写死excel绝对路径可执行"
    excel = ReadXlsData(args.filename)
    case_detail = excel.get_case_data()
    case_name = case_detail["case_name"]
    project = case_detail["project"]
    conf_path = Config(project, args.conf)
    case_list = case_detail["case_list"]
    env = conf_path.conf_path
    global_variable = case_detail["base"]["global_variable"]
    run_case_time = _time()

    @pytest.fixture(autouse=True)
    def setup(self, request):
        # 在每个测试用例开始前执行的方法
        # 判断用例是否需要执行,对需要执行的用例进行函数和sql相关的初始化操作
        is_run = request.node.get_closest_marker("parametrize").args[1][
            request.node.callspec.indices["case"]
        ]["is_run"]
        if is_run == "是":
            setup_data = request.node.get_closest_marker("parametrize").args[1][
                request.node.callspec.indices["case"]
            ]["setup"]
            allure.attach("{}".format(setup_data), "前置步骤处理结果")
            setupteardown.func_run(args.filename, setup_data, TestSuite.global_variable)
            setupteardown.sql_run(
                setup_data,
                TestSuite.case_detail["project"],
                args.conf,
                TestSuite.global_variable,
            )
        else:
            pytest.skip("此测试用例不需要执行")

    @pytest.fixture(autouse=True)
    def teardown(self, request):
        # 对用例执行完成后进行后置处理,如执行一些sql,或者一些以response为参数的函数处理
        yield
        if hasattr(self, "response"):
            teardown_data = request.node.get_closest_marker("parametrize").args[1][
                request.node.callspec.indices["case"]
            ]["teardown"]
            allure.attach("{}".format(teardown_data), "后置步骤处理结果")
            setupteardown.func_run(
                args.filename, teardown_data, TestSuite.global_variable
            )
            setupteardown.sql_run(
                teardown_data,
                TestSuite.case_detail["project"],
                args.conf,
                TestSuite.global_variable,
            )

    @allure.suite(case_name)
    @allure.epic(case_name)
    @pytest.mark.parametrize(
        "case", case_list, ids=[case["case_id"] for case in case_list]
    )
    def test_case(self, case):
        (
            case_id,
            title,
            is_run,
            model,
            level,
            desc,
            domain,
            api,
            method,
            headers,
            cookies,
            param,
            body,
            setup,
            teardown,
            extract_data,
            expected_data,
            response,
            black_list,
        ) = case.values()
        # allure 报告内容展示
        allure.dynamic.title(title)
        allure.attach("{}".format(level), "用例等级")
        allure.attach("{}".format(model), "所属模块")
        # 对部分含变量的参数初始化
        param = resolve_vars(param, TestSuite.global_variable)
        body = resolve_vars(body, TestSuite.global_variable)
        headers = resolve_vars(headers, TestSuite.global_variable)
        cookies = resolve_vars(cookies, TestSuite.global_variable)
        api = resolve_vars(api, TestSuite.global_variable)
        # 动态载入pytest_html的description
        desc = desc if desc is not None else "暂无描述"
        allure.dynamic.description(desc)
        # 初始化接口请求类
        request = RequestInterface()
        self.response = request.http_request(
            interface_domain=domain,
            interface_api=api,
            headers=headers,
            cookies=cookies,
            interface_param=body,
            interface_query=param,
            request_type=method,
        )
        log.info("步骤结束 <- 请求成功,返回response")
        self._assert = Assertions(
            TestSuite.case_detail["project"], args.conf, TestSuite.global_variable
        )
        allure.attach("{}".format(expected_data), "用例断言")
        # 结果断言
        assert self._assert.assert_method(self.response, expected_data)
        # 参数提取
        extract(self.response, extract_data, TestSuite.global_variable)


if __name__ == "__main__":
    # 运行测试用例
    if args.type == "debug":
        pytest.main(
            [
                "-q",  # 减少输出信息，只显示关键信息
                "-v",  # 启用详细模式,显示每个测试函数的完整路径和执行结果，便于了解具体哪个测试在运行
                "--cache-clear",  # 清除 pytest 缓存
                "--pyargs",
                "ytest.utils.case.test_default_case",  # 注意这里的格式
                "--disable-warnings",  # 禁用测试中的警告输出
                "--tb=short",  # 控制错误输出的回溯信息格式,short 选项会显示简短的回溯信息，方便快速浏览错误原因。你也可以选择 long（详细）或 line（仅显示错误所在的行）
                "-x",  # 遇到第一个失败后立即停止测试
                # '--pdb'
            ]
        )
    else:
        pytest.main(
            [
                "-s",
                "-v",
                "--cache-clear",  # 清除 pytest 缓存
                "-o log_cli=true",
                "-o log_cli_level=INFO",
                "--tb=short",
                "--pyargs",
                "ytest.utils.case.test_default_case",  # 注意这里的格式
                f"--alluredir=report/{TestSuite.project}/{args.conf}/{TestSuite.run_case_time}/xml",  # 报告的路径
            ]
        )
