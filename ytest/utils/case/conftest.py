#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :conftest.py
@说明        : pytest的配置
@时间        :2023/04/24 17:56:49
@作者        :Leo
@版本        :1.0
"""
import pytest
import importlib
import inspect
import types

from ytest.common.allure.environment import (
    add_environment,
    add_categories,
    add_history_trend,
)
from ytest.common.control.shell import Shell


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


def pytest_configure(config):
    """
    在pytest 运行前被调用一次，主要用于在测试运行之前进行配置和初始化工作。
    """
    pass


def pytest_collection_modifyitems(config, items):
    """
    遍历并执行指定模块中的所有函数。

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
                if any(
                    param.default != inspect.Parameter.empty
                    for param in params.values()
                ):
                    # 执行函数并捕获结果
                    result = obj()
                    # 将结果添加到 hook_result 列表中
                    hook_result[f"public_{name}"] = result
            except Exception as e:
                print(f"执行函数 {name} 时发生错误: {e}")
                continue
    for item in items:
        item.cls.global_variable.update(hook_result)


def pytest_runtest_setup(item):
    """
    pytest内置函数:在执行测试用例的 setup 部分之前调用,暂时空置,没做任何功能,预留入口
    """
    request_object = item._request
    setup_data = request_object.node.get_closest_marker("parametrize").args[1][
        request_object.node.callspec.indices["case"]
    ]["setup"]


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
    # 使用生成器表达式来判断
    alluredir_args = [
        arg for arg in session.config.invocation_params.args if "--alluredir" in arg
    ]
    if len(alluredir_args) > 0:
        args = alluredir_args[0]
        # 解析参数
        _, report_dir = args.split("--alluredir=")
        values = report_dir.split("/")
        # 输出结果
        project, conf, run_case_time = values[1], values[2], values[3]
        # 添加环境配置展示
        add_environment(project, f"report/{project}/{conf}/{run_case_time}")
        # 添加用例异常分类展示
        add_categories(f"report/{project}/{conf}/{run_case_time}")
        # 生成 Allure 报告
        cmd = "allure generate %s -o %s --clear %s" % (
            f"report/{project}/{conf}/{run_case_time}/xml",
            f"report/{project}/{conf}/{run_case_time}/html",
            f"report/{project}/{conf}/{run_case_time}",
        )
        Shell.invoke(cmd)
        # 添加用例的历史执行情况展示
        if run_case_time != "debug":
            add_history_trend(f"report/{project}/{conf}/", run_case_time)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    1. 预留入口,用于修改用例执行完成还没生成allure的数据时变更数据的入口
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # 检查测试项是否有参数
        if "case" in item.fixturenames:
            # 从报告中删除参数部分
            report.sections = [
                section for section in report.sections if "Parameters" not in section
            ]
