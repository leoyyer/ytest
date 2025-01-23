#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :conftest.py
@说明        : pytest的配置
@时间        :2023/04/24 17:56:49
@作者        :Leo
@版本        :1.0
"""
import pytest, importlib, inspect, types, os, re, allure
from collections import defaultdict
from ytest.common.Sqllife import ytest_db
from ytest.common.Shell import shell


# 记录模块及其下的测试用例
module_results = defaultdict(lambda: {"passed": [], "failed": [], "skipped": []})

BLACK_LIST = {}
GLOBAL_VARIABLE = {}


@pytest.fixture(scope="session")
# 整个测试会话(session)中只执行一次 fixture 函数。
def global_variable():
    """预设一些全局变量"""
    GLOBAL_VARIABLE = {"1": 2}
    return {"GLOBAL_VARIABLE": GLOBAL_VARIABLE}


@pytest.fixture(scope="session")
def global_black_list():
    """
    使用diff功能时,全局过滤一些不需要diff的字段
    """
    return BLACK_LIST


def pytest_sessionfinish(session, exitstatus):
    """
    pytest内置函数:在测试会话结束时调用
    1. 获取pytest的执行命令,提取出对应的项目,配置,运行用例时间
    2. 对报告做修改主要有:
        * 添加环境配置展示
        * 添加用例异常分类展示
        * 生成 Allure 报告
        * 添加用例的历史执行情况展示
    """
    # 获取命令行参数的值
    alluredir_args = [arg for arg in session.config.invocation_params.args if "--alluredir" in arg]
    if len(alluredir_args) > 0:
        args = alluredir_args[0]
        # 解析参数
        _, report_dir = args.split("--alluredir=")
        # 规范化路径，分割路径成不同部分，兼容 Windows 和 Linux
        normalized_path = os.path.normpath(report_dir)
        values = normalized_path.split(os.sep)
        # 提取项目名、配置名、运行时间和报告ID
        project, conf, run_case_time = (values[1], values[2], values[3])
        if run_case_time in ["debug"]:
            xml_path = os.path.join("report", project, conf, run_case_time, "allure-results")
            html_path = os.path.join("report", project, conf, run_case_time, "allure-report")
            clear_path = os.path.join("report", project, conf, run_case_time)
            cmd = f"allure generate {xml_path} -o {html_path} --clear {clear_path}"
            shell.invoke(cmd)


def pytest_configure(config):
    """
    在pytest 运行前被调用一次，主要用于在测试运行之前进行配置和初始化工作。
    """
    pass


def pytest_collection_modifyitems(config, items):
    """
    1.遍历并执行指定模块中的所有函数,加入到全局变量中
    2.自定义 pytest 终端报告格式,不展示参数化的数据
    Args:
        module_name (str): 模块名，例如 "public"
    """
    try:
        # 动态导入模块
        module = importlib.import_module("public")
    except ModuleNotFoundError:
        print("模块 public 不存在.")
        return
    hook_result = {}
    for name in dir(module):
        obj = getattr(module, name)
        # 确保对象是可调用的函数
        if callable(obj) and isinstance(obj, types.FunctionType):
            try:
                # 获取函数的参数列表
                params = inspect.signature(obj).parameters
                # 检查是否有参数具有默认值
                if any(param.default != inspect.Parameter.empty for param in params.values()):
                    # 执行函数并捕获结果
                    result = obj()
                    # 将结果添加到 hook_result 列表中
                    hook_result[f"public_{name}"] = result
            except Exception as e:
                print(f"执行函数 {name} 时发生错误: {e}")
                continue
    for item in items:
        item.cls.global_variable.update(hook_result)
    for item in items:
        if hasattr(item, "callspec"):
            # 提取参数中的 `title`
            case = item.callspec.params.get("case")
            if case:
                title = case.get("title", "No Title")
                # 将 `_nodeid` 设为 `title`，用于显示
                item._nodeid = title


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """
    pytest内置函数:在执行测试用例的 setup 部分之前调用,暂时空置,没做任何功能,预留入口
    """
    yield
    request_object = item._request
    setup_data = request_object.node.get_closest_marker("parametrize").args[1][request_object.node.callspec.indices["case"]]["setup"]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    1. 预留入口,用于修改用例执行完成还没生成allure的数据时变更数据的入口
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # 动态设置 Allure 的标题
        case = item.callspec.params.get("case") if hasattr(item, "callspec") else None
        if case and "title" in case:
            allure.dynamic.title(case["title"])
        # 移除 Allure 报告中的参数
        report.user_properties = []
    if report.when == "call":
        # 如果存在 Allure 报告的参数，则清空它
        if hasattr(report, "user_properties"):
            report.user_properties = []


def pytest_runtest_logreport(report):
    """捕获测试结果并归类到对应模块"""
    if report.when == "call":  # 只关心测试函数的执行结果
        module_name = report.nodeid.split("::")[0]  # 提取模块名称
        if report.outcome == "passed":
            module_results[module_name]["passed"].append(report.nodeid)
        elif report.outcome == "failed":
            module_results[module_name]["failed"].append(report.nodeid)
        elif report.outcome == "skipped":
            module_results[module_name]["skipped"].append(report.nodeid)


def pytest_terminal_summary(config):
    """在测试结束时按模块输出统计信息"""
    # 获取 pytest 命令行参数
    option = config.option  # 通过 config 访问命令行的所有参数
    allure_report_dir = option.allure_report_dir  # 提取 allure_report_dir
    # 规范路径，兼容 Linux 和 Windows
    normalized_path = os.path.normpath(allure_report_dir)
    # 分割路径并提取最后一个含有数字的部分
    run_type = normalized_path.split(os.sep)[-2]
    if run_type not in ["debug"]:
        parts = normalized_path.split(os.sep)
        # 匹配最后一个由纯数字组成的部分,提取最后_后的数字
        report_id = parts[-2].split("_")[-1]
        for module, results in module_results.items():
            ytest_db.insert_api_detail(
                report_id,
                module,
                len(results["passed"]),
                len(results["failed"]),
                len(results["skipped"]),
            )
