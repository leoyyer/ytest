#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :environment.py
@说明        :allure报告添加环境描述
@时间        :2021/08/30 14:51:46
@作者        :Leo
@版本        :1.0
'''
from jinja2 import Environment, FileSystemLoader
from common.conf import Config



def add_environment(project, path):
    """[summary]
    allure报告首页overview-环境变量设置处不支持中文
    Args:
        path ([type]): [description]
    """
    conf = Config(project=project)
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template('environment')
    base_url = conf.get_conf("project", 'base_url')
    project_name = conf.get_conf("project", 'project_name')
    project_team = conf.get_conf('project', "project_team")
    tester = conf.get_conf('project', 'tester')
    # 生成对应的用例名
    filename = 'environment.properties'
    # 模版内容生成
    content = template.render(base_url=base_url, project_name=project_name, project_team=project_team, tester=tester)
    with open(path + '/' + filename, 'w', encoding='utf-8') as fp:
        fp.write(content)
        fp.close()


if __name__ == '__main__':
    add_environment('/Users/leo/workspace/mingyuanyun/Api_Automation_Test/Report/api/2021-08-30/14-41-58/allure')