#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :__main__.py
@说明        : ytest命令行封装
@时间        :2022/02/09 14:53:59
@作者        :Leo
@版本        :1.0
'''
import click
import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from backup_sql import sql_backup
from tools.fuzz_params.read_excel import ReadXlsData
from common.execution.routine.routine_run import RoutuneRun
from common.execution.process.process_run import ProCessRun
from common.execution.update_excel.update_excel_run import UpdataExcelRun
from sql.sql_plan import run as Initialize_auto_database


__version__ = "1.0.0"


def verbose_option(f):
    def callback(ctx, param, value):
        pass

    return click.option("-v", "--version",
                        is_flag=True,
                        expose_value=False,
                        help="Enable verbose output",
                        callback=callback)(f)


def common_options(f):
#    f = verbose_option(f)
    return f


pgk_dir = os.path.dirname(os.path.abspath(__file__))
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    '{0} from {1} (Python {2})'.format(__version__, pgk_dir, sys.version[:3]),
    '-v', '--version')
@common_options
def cli():
    """
    Welcome to this tool.\nwhich is suitable for interface automation testing, scenario automation testing.
    """


# 自定义功能：db重置
@cli.command(name="db", help="""drop database""")
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def db_command():
    Initialize_auto_database()
    click.echo("The database was drop successfully")


# 自定义功能：用例膨胀
@cli.command(name="swell", help="""Use cases are automatically generated based on fuzzy parameters""")
@click.option('-p', '--project', required=True, help="The project that needs to generate the use case")
@click.option('-d', '--domain', required=True, help="Specify a domain under the project")
@click.option('-n', '--name', required=True, help="Do you need to clean up old use cases")
@click.option('-nu', '--number', required=False, help="Specify the number of use case lines that need fuzzy generation")
def swell_command(project, domain, name, number):
    filename = f"{base_path}/data/{project}/api/{domain}/{name}.xlsx"
    if os.path.exists(filename):
        if number:
            data = ReadXlsData(filename, number)
        else:
            data = ReadXlsData(filename)
        data.add_case()
        print("Use case generated successfully")
    else:
        click.echo("error, filename is not exists")


# 自定义功能：生成用例
@cli.command(name="create", help="""Generate test cases under the project""")
@click.option('-p', '--project', required=True, help="The project that needs to generate the use case")
@click.option('-t', '--type', required=True, type=click.Choice(['api', 'suite']), help='The type of use case that needs to execute the project')
@click.option('-c', '--clear', required=False, help="Do you need to clean up old use cases", default=False)
@click.option('-tp', '--template', required=False, help="Specify a template for generating use cases")
def create_command(project, type, template, clear):
    run_case = RoutuneRun(project=project, type=type, template=template)
    run_case.regenerate_case()
    click.echo("Use case created successfully ")


# 自定义功能：debug用例
@cli.command(name="debug", help="""debug case """)
@click.option('-p', '--project', required=True, help="Project name to be executed")
@click.option('-t', '--type', required=False, type=click.Choice(['all', 'api', 'suite']), help='The type of use case that needs to execute the project')
@click.option('-f', '--filename', help='Specify a domain under the project', default="")
@click.option('-tp', '--template', required=False, help="Specify a template for generating use cases")
@click.option('--env', required=False, help='The configuration read during execution, the default is: conf', default='conf')
@click.option('--db', required=False, type=click.Choice(['true']), help='Do you want to clear the database')
@click.option('--report', required=False, type=click.Choice(['True', 'False']), help='Whether a report needs to be generated', default='False')
@click.option('-process', '--process', required=False, type=click.Choice(['True']), help="pytest run by Process")
def debug_command(project, type, template, filename, report, env, db, process):
    if process == "True":
        run_case = ProCessRun(project=project, type=type, template=template, isreport=report, filename=filename, env=env)
    else:
        run_case = RoutuneRun(project=project, type=type, template=template, isreport=report, filename=filename, env=env)
    if db == 'true':
        Initialize_auto_database()
    run_case.run_case()


# 自定义功能：执行用例
@cli.command(name="run", help="""run case """)
@click.option('-p', '--project', required=True, help="Project name to be executed")
@click.option('-t', '--type', required=False, type=click.Choice(['all', 'api', 'suite']), help='The type of use case that needs to execute the project')
@click.option('-f', '--filename', help='Specify a domain under the project', default="")
@click.option('-tp', '--template', required=False, help="Specify a template for generating use cases")
@click.option('--env', required=False, help='The configuration read during execution, the default is: conf', default='conf')
@click.option('--db', required=False, type=click.Choice(['true']), help='Do you want to clear the database')
@click.option('-process', '--process', required=False, type=click.Choice(['True']), help="pytest run by Process")
def run_command(project, type, template, filename, env, db, process):
    if process == "True":
        run_case = ProCessRun(project=project, ploy='run', type=type, template=template, isreport="True", filename=filename, env=env)
    else:
        run_case = RoutuneRun(project=project, ploy='run', type=type, template=template, isreport="True", filename=filename, env=env)
    if db == 'true':
        Initialize_auto_database()
    run_case.run_case()


# 自定义功能:冒烟测试
@cli.command(name="smoke", help="smoke case")
@click.option('-p', '--project', required=True, help="Project name to be executed")
@click.option('-t', '--type', required=False, type=click.Choice(['all', 'api', 'suite']), help='The type of use case that needs to execute the project')
@click.option('-f', '--filename', help='Specify a domain under the project', default="")
@click.option('-tp', '--template', required=False, help="Specify a template for generating use cases")
@click.option('--env', required=False, help='The configuration read during execution, the default is: smoke', default='smoke')
@click.option('--db', required=False, type=click.Choice(['true']), help='Do you want to clear the database')
@click.option('-process', '--process', required=False, type=click.Choice(['True']), help="pytest run by Process")
def smoke_command(project, type, template, filename, env, db, process):
    if process == "True":
        run_case = ProCessRun(project=project, ploy='run', type=type, template=template, isreport="True", filename=filename, env=env)
    else:
        run_case = RoutuneRun(project=project, ploy='run', type=type, template=template, isreport="True", filename=filename, env=env)
    if db == 'true':
        Initialize_auto_database()
    run_case.run_case()


# 自定义功能:冒烟测试
@cli.command(name="assert", help="assert case")
@click.option('-p', '--project', required=True, help="Project name to be executed")
@click.option('-t', '--type', required=True, type=click.Choice(['api', 'suite']), help='The type of use case that needs to execute the project')
@click.option('-f', '--filename', required=True, help='Specify a domain under the project', default="")
@click.option('-tp', '--template', required=False, help="Specify a template for generating use cases", default='case_template_json_diff')
@click.option('--env', required=False, help='The configuration read during execution, the default is: conf', default='conf')
@click.option('--report', required=False, type=click.Choice(['True', 'False']), help='Whether a report needs to be generated', default='False')
@click.option('--exc', required=True, help='Enter the test case that needs to be updated')
def assert_command(project, type, filename, report, template, env, exc):
    test = UpdataExcelRun(project=project, type=type, ploy='debug', filename=filename, isreport=report, template=template, env=env, excel_name=exc)
    test.run_case()




if __name__ == '__main__':
    cli()
