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
from ytest.utils.runner.run import multi_process_run,run
from ytest.utils.initializer.project_initializer import ProjectInitializer


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
def main():
    """
    Welcome to this tool.\nwhich is suitable for interface automation testing, scenario automation testing.
    """

# 自定义功能：执行用例
@main.command(name="run", help="""run case """)
@click.option('-p', '--project', required=True, help="Project name to be executed")
@click.option('-t', '--type', required=False, type=click.Choice(['all', 'api', 'suite']), help='The type of use case that needs to execute the project')
@click.option('-f', '--filename', help='Specify a domain under the project', default="")
@click.option('--env', required=False, help='The configuration read during execution, the default is: conf', default='conf')
@click.option('-process', '--process', required=False, type=click.Choice(['True']), help="pytest run by Process")
def run_command(project, type, filename, env, process):
    if process == "True":
        project = os.path.join('case', project)
        multi_process_run(project=project, floder=type, conf=env)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(base_dir, 'case', project, type, f'{filename}.xlsx')
        run(script_path,env)


# 脚手架创建

@main.command(name="create", help="""create auto project """)
@click.option('-p', '--project', required=True, help="Project name to be executed")
def run_command(project):
    project_initializer = ProjectInitializer(project)
    project_initializer.initialize_project()



if __name__ == '__main__':
    main()
