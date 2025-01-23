#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :project_initializer.py
@说明        :手脚架初始化
@时间        :2024/07/19 16:45:54
@作者        :Leo
@版本        :1.0
"""

import os
import shutil
from ytest.templates.hook_temp import hook_content
from ytest.templates.public_temp import public_content
from ytest.templates.ini_temp import ini_content

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProjectInitializer:
    def __init__(self, project_name):
        self.project_name = project_name
        self.base_path = os.path.abspath(os.getcwd())
        self.ini_content = ini_content
        self.hook_content = hook_content
        self.public_content = public_content
        self.case_dir = os.path.join(self.base_path, "case")
        self.project_dir = os.path.join(self.case_dir, project_name)
        self.api_dir = os.path.join(self.project_dir, "api")
        self.suite_dir = os.path.join(self.project_dir, "suite")
        self.ini_files = ["default.ini", "test.ini", "beta.ini", "prod.ini"]
        self.hook_file = os.path.join(self.project_dir, "hook.py")
        self.public_file = os.path.join(self.case_dir, "public.py")
        self.demo_api_file = os.path.join(base_dir, "templates", "demo_api.xlsx")
        self.demo_suite_file = os.path.join(base_dir, "templates", "demo_suite.xlsx")

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass

    def create_file(self, path, content):
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content)
        else:
            pass

    def copy_demo_file(self):
        if os.path.exists(self.demo_api_file) or os.path.exists(self.demo_suite_file):
            api_dest_file = os.path.join(self.api_dir, "demo_api.xlsx")
            suite_dest_file = os.path.join(self.suite_dir, "demo_suite.xlsx")
            if not os.path.exists(api_dest_file):
                shutil.copy(self.demo_api_file, api_dest_file)
            else:
                pass
            if not os.path.exists(suite_dest_file):
                shutil.copy(self.demo_suite_file, suite_dest_file)
            else:
                pass

        else:
            pass

    def initialize_project(self):
        # 创建文件夹
        self.create_dir(self.case_dir)
        self.create_dir(self.project_dir)
        self.create_dir(self.api_dir)
        self.create_dir(self.suite_dir)
        # 创建 ini 文件
        for ini_file in self.ini_files:
            file_path = os.path.join(self.project_dir, ini_file)
            self.create_file(file_path, self.ini_content)
        # 创建 hook.py 文件
        self.create_file(self.hook_file, self.hook_content)
        # 创建 public.py 文件
        self.create_file(self.public_file, self.public_content)
        # 拷贝 demo.xlsx 文件
        self.copy_demo_file()
        print(f"项目{self.project_name}初始化成功!")


if __name__ == "__main__":
    project_initializer = ProjectInitializer("demo")
    project_initializer.initialize_project()
