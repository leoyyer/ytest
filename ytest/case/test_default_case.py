#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pytest, argparse, os, allure
from ytest.config.ConfFile import ConfigFile
from ytest.common.Excel import ReadXlsData
from ytest.common.Logger import logger
from ytest.case.setupteardown import setupteardown
from ytest.common.HookVariable import hook_variable
from ytest.common.Api import RequestInterface
from ytest.case.asserts import Assertions
from ytest.common.Time import ytest_time
from ytest.common.File import file_operate


parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help="配置所需执行的用例路径")
parser.add_argument("--conf", type=str, help="配置指定的执行文件", default="default")
parser.add_argument("--type", type=str, help="执行策略", default="")
parser.add_argument("--date", type=str, help="多线程执行时,指定的报告路径", default="")
parser.add_argument("--report_id", type=str, help="多线程执行时,报告id", default="")
args = parser.parse_args()
log = logger


class TestSuite(object):
    # args.filename = "调试入口,写死excel绝对路径可执行"
    excel = ReadXlsData(args.filename)
    case_detail = excel.get_case_data()
    case_name = case_detail["case_name"]
    project = case_detail["project"]
    conf_path = ConfigFile(project, args.conf)
    case_list = case_detail["case_list"]
    env = conf_path.conf_path
    global_variable = case_detail["base"]["global_variable"]
    run_case_time = ytest_time._time()

    @pytest.fixture(autouse=True)
    def setup(self, request):
        # 在每个测试用例开始前执行的方法
        # 判断用例是否需要执行,对需要执行的用例进行函数和sql相关的初始化操作
        is_run = request.node.get_closest_marker("parametrize").args[1][request.node.callspec.indices["case"]]["is_run"]
        if is_run == "是":
            setup_data = request.node.get_closest_marker("parametrize").args[1][request.node.callspec.indices["case"]]["setup"]
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
            teardown_data = request.node.get_closest_marker("parametrize").args[1][request.node.callspec.indices["case"]]["teardown"]
            allure.attach("{}".format(teardown_data), "后置步骤处理结果")
            setupteardown.func_run(args.filename, teardown_data, TestSuite.global_variable)
            setupteardown.sql_run(
                teardown_data,
                TestSuite.case_detail["project"],
                args.conf,
                TestSuite.global_variable,
            )

    @allure.suite(case_name)
    @allure.epic(case_name)
    @pytest.mark.parametrize("case", case_list, ids=[case["case_id"] for case in case_list])
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
        _title = case["title"]
        allure.dynamic.title(_title)
        allure.attach("{}".format(level), "用例等级")
        allure.attach("{}".format(model), "所属模块")
        allure.attach("{}".format(TestSuite.global_variable), "全局变量")
        # 对部分含变量的参数初始化
        param = hook_variable.resolve_vars(param, TestSuite.global_variable)
        body = hook_variable.resolve_vars(body, TestSuite.global_variable)
        headers = hook_variable.resolve_vars(headers, TestSuite.global_variable)
        cookies = hook_variable.resolve_vars(cookies, TestSuite.global_variable)
        api = hook_variable.resolve_vars(api, TestSuite.global_variable)
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
        self._assert = Assertions(TestSuite.case_detail["project"], args.conf, TestSuite.global_variable, args.filename)
        allure.attach("{}".format(expected_data), "用例断言")
        # 结果断言
        assert self._assert.assert_method(self.response, expected_data)
        # 参数提取
        setupteardown.extract(self.response, extract_data, TestSuite.global_variable)


if __name__ == "__main__":
    # 运行测试用例
    if args.type == "debug":
        # 生成路径，兼容 Linux 和 Windows
        debug_report_path = os.path.join("report", TestSuite.project, args.conf, "debug")
        file_operate.default_folder(debug_report_path)

        pytest.main(
            [
                "-q",  # 减少输出信息，只显示关键信息
                "-v",  # 启用详细模式
                "--cache-clear",  # 清除 pytest 缓存
                "--pyargs",
                "ytest.case.test_default_case",  # 注意这里的格式
                "--disable-warnings",  # 禁用测试中的警告输出
                "--tb=short",  # 错误输出的回溯信息格式
                "-x",  # 遇到第一个失败后立即停止测试
                f"--alluredir={os.path.join(debug_report_path, 'xml')}",  # 报告的路径
            ]
        )
    elif args.date:
        # 生成路径，兼容 Linux 和 Windows
        date_report_path = os.path.join("report", TestSuite.project, args.conf, args.date, args.report_id, "xml")

        pytest.main(
            [
                "-q",  # 安静模式运行
                "--cache-clear",  # 清除 pytest 缓存, 确保测试环境干净
                "-o",
                "log_cli=true",
                "-o",
                "log_cli_level=INFO",  # 控制台中显示INFO级别的日志
                "--tb=short",
                "--disable-warnings",  # 禁用测试中的警告输出
                "--reruns",
                "3",  # 失败用例重试次数为3次
                "--maxfail=3",  # 3个失败之后停止测试
                "--pyargs",
                "ytest.case.test_default_case",  # 注意这里的格式
                f"--alluredir={date_report_path}",  # 报告的路径
            ]
        )
    else:
        # 生成路径，兼容 Linux 和 Windows
        default_report_path = os.path.join("report", TestSuite.project, args.conf, TestSuite.run_case_time, "xml")

        pytest.main(
            [
                "-q",  # 安静模式运行
                "--cache-clear",  # 清除 pytest 缓存, 确保测试环境干净
                "-o",
                "log_cli=true",
                "-o",
                "log_cli_level=INFO",  # 控制台中显示INFO级别的日志
                "--tb=short",
                "--disable-warnings",  # 禁用测试中的警告输出
                "--maxfail=3",  # 3个失败之后停止测试
                "--pyargs",
                "ytest.case.test_default_case",  # 注意这里的格式
                f"--alluredir={default_report_path}",  # 报告的路径
            ]
        )
