#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :__main__.py
@说明        : ytest命令行封装
@时间        :2022/02/09 14:53:59
@作者        :Leo
@版本        :1.0
"""
import click, os, sys
from ytest.common.Run import multi_process_run, run
from ytest.initializer.project_initializer import ProjectInitializer
from ytest.common.CaseBlowUp import CaseBlowUp
from ytest.conf import config
from ytest.common.Sqllife import ytest_db


__version__ = "1.0.0"


def verbose_option(f):
    def callback(ctx, param, value):
        pass

    return click.option(
        "-v",
        "--version",
        is_flag=True,
        expose_value=False,
        help="Enable verbose output",
        callback=callback,
    )(f)


def common_options(f):
    #    f = verbose_option(f)
    return f


pgk_dir = os.path.dirname(os.path.abspath(__file__))


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(
    "{0} from {1} (Python {2})".format(__version__, pgk_dir, sys.version[:3]),
    "-v",
    "--version",
)
@common_options
def main():
    """
    Welcome to this tool.\nwhich is suitable for interface automation testing, scenario automation testing.
    """


# 自定义功能：debug用例
@main.command(name="debug", help="""debug测试用例 """)
@click.option("-p", "--project", required=True, help="Project name to be executed")
@click.option(
    "-t",
    "--type",
    required=False,
    type=click.Choice(["all", "api", "suite"]),
    help="The type of use case that needs to execute the project",
)
@click.option("-f", "--filename", help="Specify a domain under the project", default="")
@click.option(
    "--env",
    required=False,
    help="The configuration read during execution, the default is: conf",
    default="conf",
)
def run_command(project, type, filename, env):
    script_path = os.path.join(config.case_path, project, type, f"{filename}.xlsx")
    run(script_path, env, run_type="debug")


# 自定义功能：执行用例
@main.command(name="run", help="""运行测试用例 """)
@click.option("-p", "--project", required=True, help="Project name to be executed")
@click.option(
    "-t",
    "--type",
    required=False,
    type=click.Choice(["all", "api", "suite"]),
    help="The type of use case that needs to execute the project",
)
@click.option("-f", "--filename", help="Specify a domain under the project", default="")
@click.option(
    "--env",
    required=False,
    help="The configuration read during execution, the default is: conf",
    default="conf",
)
@click.option(
    "-process",
    "--process",
    required=False,
    type=click.Choice(["True"]),
    help="pytest run by Process",
)
def run_command(project, type, filename, env, process):
    if process == "True":
        project = os.path.join("case", project)
        multi_process_run(project=project, ytest_folder=type, conf=env)
    else:
        script_path = os.path.join(config.case_path, project, type, f"{filename}.xlsx")
        run(script_path, env)


# 脚手架创建
@main.command(name="create", help="""创建自动化项目 """)
@click.option("-p", "--project", required=True, help="Project name to be executed")
def run_command(project):
    project_initializer = ProjectInitializer(project)
    project_initializer.initialize_project()
    ytest_db._create_tables()


# 用例膨胀
@main.command(name="add", help="""对api用例进行膨胀""")
@click.option("-p", "--project", required=True, help="请输入项目名称")
@click.option("-f", "--filename", required=True, help="请输入api用例名[excel名称]")
@click.option(
    "-v", "--value", required=True, help="请输入需要膨胀的参数,仅支持body/param"
)
def run_command(project, filename, value):
    # 使用三元表达式检查并修改文件名
    filename = filename if filename.endswith(".xlsx") else f"{filename}.xlsx"
    api_case = CaseBlowUp(project, filename, value)
    api_case.parse_excel_and_generate_tests()
    print(f"执行成功,请重新打开用例{filename}查看")


if __name__ == "__main__":
    main()
