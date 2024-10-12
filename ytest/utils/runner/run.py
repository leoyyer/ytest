#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :run.py
@说明        : 支持多进程运行(每个进程间的变量不互通)
@时间        :2023/05/11 18:24:32
@作者        :Leo
@版本        :1.0
"""
import subprocess
import os
from multiprocessing import Pool
from functools import partial
from ytest.utils.case.case_file import get_file_path, find_file
from ytest.utils.tools._time import _dateTime
from ytest.common.control.shell import Shell


global_project = None  # 定义一个全局变量


def multi_process_run(project, floder=None, conf=None):
    """
    0. 判断项目和所需运行的文件夹,以及配置文件是否存在
    1. 遍历用例,过滤掉名字以_stop和._的开头的用例
    2. 组装参数,废弃原来的用例是否生成判断,默认生成
    """
    case_list = get_file_path(project, floder)
    if conf:
        _conf = conf if conf is not None else "conf"
        # 验证conf.ini文件是否存在
        find_file(project, f"{_conf}.ini")
    # 生成测试报告文件夹
    now_date = _dateTime()
    POOL_SIZE = 3  # 设置最大并发进程数
    with Pool(POOL_SIZE) as pool:
        pool.map(partial(run, conf=conf, date=now_date), case_list)
    # 多进程执行完成后,需要统一生成测试报告
    project = project.split("/")[-1]
    cmd = "allure generate %s -o %s " % (
        f"report/{project}/{conf}/{now_date}/xml",
        f"report/{project}/{conf}/{now_date}/html",
    )
    Shell.invoke(cmd)


def run(filename, conf, run_type=None, date=None):
    # 获取当前脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建相对路径
    script_path = os.path.join(base_dir, "..", "case", "test_default_case.py")
    # 规范路径
    script_path = os.path.abspath(script_path)
    if not run_type:
        cmd = ["python", script_path, "--filename", filename, "--conf", conf]
    if date:
        cmd = [
            "python",
            script_path,
            "--filename",
            filename,
            "--conf",
            conf,
            "--date",
            date,
        ]

    else:
        cmd = [
            "python",
            script_path,
            "--filename",
            filename,
            "--conf",
            conf,
            "--type",
            "debug",
        ]
    subprocess.run(cmd)


if __name__ == "__main__":
    project = os.path.join("case", "demo")
    multi_process_run(project, floder="suite", conf="test")
