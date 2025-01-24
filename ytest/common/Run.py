#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :run.py
@说明        : 支持多进程运行(每个进程间的变量不互通)
@时间        :2023/05/11 18:24:32
@作者        :Leo
@版本        :1.0
"""
from icecream import ic
import os, time, subprocess
from multiprocessing import Pool
from functools import partial
from ytest.common.File import file_operate
from ytest.common.Time import ytest_time
from ytest.common.Shell import shell
from ytest.config.ConfFile import ConfigFile
from ytest.common.Message import send_message
from ytest.common.Sqllife import ytest_db
from ytest.common.Allure import yallure


def multi_process_run(project, ytest_folder=None, conf=None):
    """
    0. 判断项目和所需运行的文件夹,以及配置文件是否存在
    1. 遍历用例,过滤掉名字以_stop和._的开头的用例
    2. 组装参数,废弃原来的用例是否生成判断,默认生成
    """
    # 使用 os.path.normpath 规范化路径
    project_path = os.path.normpath(project)
    case_list = file_operate.get_file_path(project_path, ytest_folder)

    if conf:
        conf_name = conf if conf else "conf"
        # 验证 conf.ini 文件是否存在
        file_operate.find_file(project_path, f"{conf_name}.ini")

    # 获取项目名称，兼容 Windows 和 Linux
    project_name = os.path.basename(project_path)
    now_case_conf = ConfigFile(project_name, conf_name)

    # 生成测试报告文件夹
    now_date = ytest_time._dateTime()
    report_name = f"{project_name}_{int(time.time())}"
    report_id = str(
        ytest_db.insert_report(
            report_name,
            project_name,
            conf,
            now_date,
            passed=0,
            failed=0,
            skipped=0,
            error=0,
        )
    )

    # 获取报告路径
    report_path, report_html_path = file_operate.get_report_paths(
        project_name, conf_name, now_date, report_id
    )
    yallure.add_environment(project_name, report_path)
    yallure.add_categories(report_path)

    POOL_SIZE = 3  # 设置最大并发进程数
    with Pool(POOL_SIZE) as pool:
        pool.map(partial(run, conf=conf, date=now_date, report_id=report_id), case_list)

    # 生成 Allure 报告的 Shell 命令
    cmd = f"allure generate {report_path} -c -o {report_html_path} --clear"
    shell.invoke(cmd)
    yallure.add_history_trend(
        os.path.join("report", project_name, conf_name), f"{now_date}_{report_id}"
    )

    # 获取测试结果
    failed = ytest_db.fetch_api_detail(report_id)
    all_api = ytest_db.fetch_api_all(report_id)
    passed = ytest_db.fetch_api_pass_all(report_id)
    # 更新执行结果到数据库
    ytest_db.update_report(report_id, failed)
    ytest_db.close()
    # 发送消息
    if int(now_case_conf.get_conf("qywx", "Enable")) == 1 and now_case_conf.get_conf(
        "qywx", "webhook_url"
    ):
        send_message.qywx(
            now_case_conf.get_conf("qywx", "webhook_url"),
            all_api,
            passed,
            failed,
            conf_name,
        )

    open_allure_cmd = (
        f"lsof -ti :5050 | xargs kill -9 && allure open {report_path.replace('allure-results', 'allure-report')} --host 127.0.0.1 --port 5050"
        if shell.check_port_with_lsof(5050)
        else f"allure open {report_path.replace('allure-results', 'allure-report')} --host 127.0.0.1 --port 5050"
    )
    # allure serve 无法加载趋势图,暂时不使用
    # open_allure_cmd = (
    #     f"lsof -ti :5050 | xargs kill -9 && allure serve {report_path} --host 0.0.0.0 --port 5050"
    #     if shell.check_port_with_lsof(5050)
    #     else f"allure serve {report_path} --host 127.0.0.1 --port 5050"
    # )
    shell.invoke(open_allure_cmd)


def run(filename, conf, run_type=None, date=None, report_id=None):
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
            "--report_id",
            report_id,
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
    multi_process_run(project, ytest_folder="suite", conf="test")
    # conf = Config('fast', "test")
    # ic(conf.get_conf("qywx", "webhook_url"))
